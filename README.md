# 🦜 LangGraph 101: Learning Path

Welcome to my personal journey of learning **LangGraph**! This repository contains a collection of mini-projects and experiments designed to understand the core concepts of agentic workflows, state machines, and complex LLM orchestrations.

## 📁 Repository Structure

The repo is organized into focused modules, each exploring a specific LangGraph pattern:

### 1. [🤖 Autonomous Tool Calling](./Autonomous%20tool%20calling/)
An agentic workflow where the LLM can autonomously choose and execute tools to answer user queries.
- **Key Concepts**: Agent-Loop, Tool Calling, Conditional Edges.
- **Graph**: `START -> agent -> tools -> agent -> END`.

### 2. [➕ Multi-Step Summation](./a%20graph%20to%20sum%202%20numbers/)
A deterministic state-machine workflow with user input validation and retry logic.
- **Key Concepts**: State Management, Retries, Validation Nodes, Sequential Flow.
- **Graph**: `START -> input1 -> check1 -> input2 -> check2 -> result -> END`.

## 🛠️ Prerequisites

To run these projects, you will need:
- Python 3.10+
- A `.env` file in the root or respective folders with:
  ```env
  GROQ_API_KEY=your_api_key_here
  ```

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/saqlain2204/Langgraph-101.git
   cd Langgraph-101
   ```

2. Install dependencies:
   ```bash
   pip install langgraph langchain_groq python-dotenv
   ```

## 🎨 Visualizing the Workflows

Each project includes a `main.py` script that automatically generates a `graph.png` using Mermaid. This helps in understanding the underlying architecture of the state machine at a glance.

---
*Happy Coding with LangGraph! 🚀*
