# AI Agent Scheduler

**Version:** 0.1.0  
**Description:** A modular multi-agent system designed to handle intelligent task and schedule planning using LLMs and reactive graph-based coordination.

## Overview

**AI Agent Scheduler** is a multi-AI agent system built using `FastAPI`, `LangChain`, and `LangGraph`. It leverages multiple specialized agents to collaboratively plan and optimize daily or weekly schedules based on user input, preferences, and contextual data.

This project is suitable for building AI-powered personal assistants or advanced task planners with modular, extensible architecture.

---

## Features

- ✅ Multi-agent collaboration using LangGraph
- 🧠 LLM integration via LangChain and Google Generative AI
- ⚡ Fast and responsive API with FastAPI + Uvicorn
- 📅 Intelligent scheduling based on natural language input
- 📚 Modular structure for extending agents (e.g., weather, health, meals, work)
- 🛠️ PostgreSQL integration via psycopg2-binary for data storage

---

## Technologies Used

- **Python ≥ 3.13**
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Generative AI](https://ai.google.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## Installation

### Prerequisites

- Python 3.13 or higher
- PostgreSQL (optional, for storing history or planning data)

### Setup

```bash
git clone https://github.com/chikaturin/schegent-AIagent.git
cd schegent-AIagent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

create file .env

```bash
GOOGLE_API_KEY=
MONGO_DB_URI=

DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=
HUGGINGFACE_TOKEN=
```
