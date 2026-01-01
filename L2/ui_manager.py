#!/usr/bin/env python3
"""
NAT UI Manager - Robust UI launcher with error handling and validation
"""
import subprocess
import time
import os
import sys
import atexit
import socket
from pathlib import Path

class UIManager:
    """Manages the NAT UI server lifecycle with robust error handling."""
    
    def __init__(self):
        self.ui_path = Path("NeMo-Agent-Toolkit-UI")
        self.ui_process = None
        self.ui_port = 3000
        self.nat_port = 8000
        
        # Register cleanup on exit
        atexit.register(self._cleanup)
    
    def _check_command_exists(self, command):
        """Check if a command is available."""
        try:
            subprocess.run([command, "--version"], 
                          capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _check_port_available(self, port):
        """Check if a port is available."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('localhost', port))
            return result != 0  # Port is available if connection fails
        finally:
            sock.close()
    
    def _wait_for_port(self, port, timeout=60):
        """Wait for a port to become active."""
        print(f"⏳ Waiting for service on port {port}...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self._check_port_available(port):
                return True
            time.sleep(2)
        return False
    
    def _cleanup(self):
        """Cleanup on exit."""
        if self.ui_process and self.ui_process.poll() is None:
            self.ui_process.terminate()
            try:
                self.ui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ui_process.kill()
    
    def start(self):
        """Start the UI server with comprehensive error handling."""
        try:
            # 1. Validate prerequisites
            print("🔍 Checking prerequisites...")
            
            if not self._check_command_exists("git"):
                raise RuntimeError("❌ git is not installed")
            
            if not self._check_command_exists("node"):
                raise RuntimeError("❌ Node.js is not installed")
            
            if not self._check_command_exists("npm"):
                raise RuntimeError("❌ npm is not installed")
            
            print("✅ All prerequisites found")
            
            # 2. Verify NAT server is running
            print(f"🔍 Checking NAT server on port {self.nat_port}...")
            if self._check_port_available(self.nat_port):
                print(f"⚠️  Warning: NAT server doesn't appear to be running on port {self.nat_port}")
                print("   The UI may not work properly without it")
            else:
                print(f"✅ NAT server detected on port {self.nat_port}")
            
            # 3. Check if UI port is available
            if not self._check_port_available(self.ui_port):
                print(f"⚠️  Port {self.ui_port} is already in use")
                response = input(f"   Try to kill existing process on port {self.ui_port}? (y/n): ")
                if response.lower() == 'y':
                    try:
                        subprocess.run(f"lsof -ti:{self.ui_port} | xargs kill -9 2>/dev/null || "
                                     f"fuser -k {self.ui_port}/tcp 2>/dev/null || true",
                                     shell=True, timeout=5)
                        time.sleep(2)
                    except:
                        pass
                    
                    if not self._check_port_available(self.ui_port):
                        raise RuntimeError(f"❌ Failed to free port {self.ui_port}")
            
            # 4. Clone UI repo if needed
            if not self.ui_path.exists():
                print("📥 Cloning NAT UI repository...")
                try:
                    subprocess.run(
                        ["git", "clone", 
                         "https://github.com/NVIDIA/NeMo-Agent-Toolkit-UI.git"],
                        check=True,
                        timeout=120,
                        capture_output=True
                    )
                    print("✅ UI repository cloned")
                except subprocess.TimeoutExpired:
                    raise RuntimeError("❌ Git clone timed out - check your internet connection")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"❌ Failed to clone repository: {e.stderr.decode()}")
            else:
                print("✅ UI repository already exists")
            
            # 5. Install dependencies with retry
            print("📦 Installing UI dependencies...")
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    subprocess.run(
                        ["npm", "ci", "--silent"],
                        cwd=self.ui_path,
                        check=True,
                        timeout=180,
                        capture_output=True
                    )
                    print("✅ Dependencies installed")
                    break
                except subprocess.TimeoutExpired:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Install timed out, retrying ({attempt + 1}/{max_retries})...")
                    else:
                        raise RuntimeError("❌ npm install timed out after retries")
                except subprocess.CalledProcessError as e:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Install failed, retrying ({attempt + 1}/{max_retries})...")
                    else:
                        raise RuntimeError(f"❌ Failed to install dependencies: {e.stderr.decode()}")
            
            # 6. Start UI server
            print("🎨 Starting UI development server...")
            try:
                self.ui_process = subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=self.ui_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env={**os.environ, "NEXT_TELEMETRY_DISABLED": "1"}
                )
            except Exception as e:
                raise RuntimeError(f"❌ Failed to start UI server: {e}")
            
            # 7. Wait for UI to be ready
            if not self._wait_for_port(self.ui_port, timeout=60):
                # Check if process crashed
                if self.ui_process.poll() is not None:
                    stdout, stderr = self.ui_process.communicate()
                    raise RuntimeError(
                        f"❌ UI server crashed during startup:\n{stderr[-500:]}"
                    )
                else:
                    raise RuntimeError(
                        f"❌ UI server did not start within 60 seconds"
                    )
            
            print(f"✅ UI started successfully on port {self.ui_port}")
            return True
            
        except RuntimeError as e:
            print(str(e))
            self.stop()
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.stop()
            return False
    
    def stop(self):
        """Stop the UI server gracefully."""
        if self.ui_process:
            print("🛑 Stopping UI server...")
            try:
                self.ui_process.terminate()
                self.ui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️  Force killing UI server...")
                self.ui_process.kill()
            finally:
                self.ui_process = None
            print("✅ UI server stopped")
    
    def get_status(self):
        """Get current status of UI server."""
        if self.ui_process is None:
            return "Not started"
        elif self.ui_process.poll() is None:
            return f"Running (PID: {self.ui_process.pid})"
        else:
            return f"Stopped (exit code: {self.ui_process.poll()})"
    
    def show_ui_link(self):
        """Display a clickable link to the UI."""
        # Check if UI is actually running
        if not self._check_port_available(self.ui_port):
            status = "✅ Running"
        else:
            status = "⚠️  Not responding"
        
        try:
            from IPython.display import HTML, display
            
            html_content = f'''
            <div style="padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 15px 0; color: #0066cc;">🚀 NAT UI Demo</h3>
                <p style="margin: 10px 0;">Experience your climate agent with a production-ready interface!</p>
                <p style="margin: 10px 0;">
                    Status: <strong>{status}</strong> | 
                    Port: <code style="background: #e0e0e0; padding: 2px 6px; border-radius: 3px;">{self.ui_port}</code>
                </p>
                <p style="margin: 10px 0;">
                    <strong>Local access:</strong> 
                    <a href="{os.environ.get('DLAI_LOCAL_URL').format(port=self.ui_port)}" target="_blank">http://localhost:{self.ui_port}</a>
                </p>
                <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                    💡 Tip: Try asking questions like "What's the temperature trend in France?"
                </p>
            </div>
            '''
            
            display(HTML(html_content))
            
        except ImportError:
            print(f"\n📍 UI Status: {status}")
            print(f"📍 Access the UI at: http://localhost:{self.ui_port}")
            print("💡 Tip: Try asking questions like 'What's the temperature trend in France?'")

# Create a global instance
ui_manager = UIManager()