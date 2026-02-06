# NeMo Agent Toolkit: Making Agents Reliable

This repository contains Jupyter notebooks and resources from the DeepLearning.AI short course **"Nvidia's NeMo Agent Toolkit: Making Agents Reliable"** taught by Brian McBrayer, Solutions Architect in Generative AI at Nvidia.

## About This Course

This course demonstrates how to transform proof-of-concept agent demos into production-ready systems using Nvidia's open-source NeMo Agent Toolkit (NAT). The course focuses on building a climate data analysis agent with professional observability, evaluation, and deployment capabilities.

## Course Overview

The NeMo Agent Toolkit provides building blocks to harden AI agents for production, working with frameworks like raw Python, LangGraph, CrewAI, and others. Through configuration-driven workflows, you'll learn to add observability, run systematic evaluations, and deploy with production features like authentication and rate limiting.

## Main Topics Covered

### L2: Your First NAT Workflow
- Introduction to configuration-driven development with NAT
- Building a climate science chatbot
- Running workflows locally
- Serving as a REST API with minimal code

### L3: Adding Intelligence with Tools
- Registering Python functions as agent tools
- Analyzing NOAA climate data programmatically
- Defining input schemas with Pydantic
- Transforming chatbots into ReAct agents

### L4: Observability with Phoenix Tracing
- Implementing OpenTelemetry tracing for agent workflows
- Visualizing agent reasoning and decision-making processes
- Tracking tool selection and execution
- Identifying performance bottlenecks for debugging

### L5: Multi-Agent Integration
- Combining NAT agents with agents from other frameworks (e.g., LangGraph)
- Framework-agnostic orchestration
- Coordinating specialized agents for complex tasks
- Building collaborative multi-agent systems

### L6: Evaluation and Performance Improvement
- Creating gold-standard evaluation datasets
- Using NAT's evaluation framework systematically
- Uncovering bugs and performance issues
- Making data-driven improvements through configuration experiments

### L7: Production Deployment with NAT UI
- Configuring authentication and rate limiting
- Enabling caching for improved performance
- Launching workflows with REST APIs
- Deploying with a professional web interface

## Key Learning Outcomes

- **Build production-ready agents** using configuration-driven workflows
- **Add observability and debugging tools** to understand agent reasoning
- **Measure and improve performance** through systematic evaluation
- **Deploy multi-agent workflows** with authentication, rate limiting, and professional interfaces
- **Integrate agents from any framework** into cohesive workflows

## Prerequisites

- Basic familiarity with Python
- Understanding of LLM application development
- Interest in building production-ready AI agents

## Climate Data Application

Throughout the course, you'll work with real-world climate data from NOAA (National Oceanic and Atmospheric Administration) to build a practical climate science assistant. The agent demonstrates how to:
- Query and analyze climate datasets
- Provide intelligent responses to climate-related questions
- Execute data analysis tools programmatically
- Scale from single-agent demos to multi-agent production systems

## Setup and Installation

1. Clone this repository:
```bash
git clone https://github.com/mjgrav2001/NemoAgentToolkit_ClimateAgent.git
cd NemoAgentToolkit_ClimateAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your NVIDIA API key:
```bash
export NVIDIA_API_KEY="your-api-key-here"
```
API keys can be obtained by creating an account at [build.nvidia.com](https://build.nvidia.com)

4. Test your environment:
```bash
bash test-environment.sh
```

## Repository Structure

```
├── L2/                     # First NAT Workflow
├── L3/                     # Adding Intelligence with Tools
├── L4/                     # Observability with Phoenix Tracing
├── L5/                     # Multi-Agent Integration
├── L6/                     # Evaluation and Improvement
├── L7/                     # Production Deployment
├── resources/
│   └── climate_data/      # NOAA climate datasets
├── requirements.txt        # Python dependencies
├── test-environment.sh    # Environment setup verification
└── README.md              # This file
```

## Resources

- **Course Page**: [DeepLearning.AI - NeMo Agent Toolkit](https://www.deeplearning.ai/short-courses/nvidia-nat-making-agents-reliable/)
- **NeMo Agent Toolkit Documentation**: [docs.nvidia.com/nemo/agent-toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)
- **Official Repository**: [NVIDIA/NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
- **NVIDIA Developer Portal**: [developer.nvidia.com/nemo-agent-toolkit](https://developer.nvidia.com/nemo-agent-toolkit)

## Technologies Used

- **NVIDIA NeMo Agent Toolkit**: Framework-agnostic agent orchestration
- **Phoenix/OpenTelemetry**: Observability and tracing
- **Pydantic**: Schema validation for tool inputs
- **LangGraph**: Multi-agent framework integration
- **NOAA Climate Data**: Real-world dataset for demonstrations
- **REST APIs**: Production deployment interfaces

## About NVIDIA NeMo Agent Toolkit

NVIDIA NeMo Agent Toolkit is an open-source library for efficiently connecting, evaluating, and optimizing teams of AI agents. It focuses on enabling developers to quickly build, evaluate, profile, and deploy agentic systems with production-grade reliability.

## Instructor

**Brian McBrayer**  
Solutions Architect in Generative AI at NVIDIA

## License

Please refer to the original course materials and NVIDIA's licensing terms for usage rights.

## Acknowledgments

This repository contains course materials from DeepLearning.AI's short course on Nvidia's NeMo Agent Toolkit. Special thanks to Andrew Ng, DeepLearning.AI, and the NVIDIA team for creating this educational content.
