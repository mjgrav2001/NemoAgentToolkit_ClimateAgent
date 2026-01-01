#!/bin/bash
# Test script to verify the environment is set up correctly

echo "=== Environment Test ==="
echo

echo "Python version:"
python --version
echo

echo "Virtual environment:"
which python
echo

echo "Node.js version:"
node -v
echo

echo "npm version:"
npm -v
echo

echo "NeMo Agent Toolkit (nat) command:"
which nat && echo "nat command is available" || echo "nat command not found"
echo

echo "Environment variables (sample):"
echo "OPENAI_API_KEY is $([ -z "$OPENAI_API_KEY" ] && echo "not set" || echo "set")"
echo "ANTHROPIC_API_KEY is $([ -z "$ANTHROPIC_API_KEY" ] && echo "not set" || echo "set")"
echo

echo "=== Test Complete ==="
