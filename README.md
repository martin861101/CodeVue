# 👁️ CodeVue (NeuroTerm v3.0)

> **The Cyberpunk AI Code Companion.**
> A terminal-based, agentic AI coding environment that remembers your projects, routes tasks intelligently, and autonomously fixes bugs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![AI](https://img.shields.io/badge/AI-Agentic-purple.svg)

---

## 🚀 Overview

CodeVue is not just a wrapper for ChatGPT. It is a fully **Agentic System** that lives in your terminal. It combines local AI (Ollama) for speed and privacy with cloud AI (Gemini/OpenRouter) for complex reasoning.

**Key Capabilities:**
* **🧠 RAG Memory:** Remembers past conversations and code context (using ChromaDB & SQLite).
* **🚦 Smart Routing:** Automatically sends simple tasks to a free local model and complex tasks to paid cloud APIs.
* **🔄 Auto-Fix Loop:** Can run a script, read the error traceback, and apply a fix autonomously until it works.
* **🛡️ Safety First:** Creates timestamped backups before every file edit.
* **📝 Live Logging:** Trace the AI's thought process in real-time.

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User Input] --> Agent[NeuroAgent Executor]
    Agent --> Memory[RAG Memory (ChromaDB)]
    Agent --> Router[NeuroGraph Router (Ollama/Llama 3.2)]
    Router -- Simple Task --> Local[Local LLM (Ollama)]
    Router -- Complex Task --> Cloud[Cloud API (Gemini/OpenRouter)]
    Local --> Response
    Cloud --> Response
    Response --> UI[Textual TUI]
    Response --> Files[File System]
    Files --> Backup[Auto-Backup (SQLite)]
```

### 🤖 Core Stack
- **Frontend:** Textual (Modern TUI framework)
- **Orchestration:** LangGraph
- **Memory:** ChromaDB + SQLite
- **Local AI:** Ollama (llama3.2, nomic-embed-text)
- **Cloud AI:** Google Gemini / OpenRouter

---

## ⚡ Installation

### Prerequisites
- Python 3.10+
- Ollama installed and running

### Setup
```bash
git clone https://github.com/yourusername/codevue.git
cd codevue
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pull Models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Configure API Keys (Optional)
```bash
export GEMINI_API_KEY="your_key"
export OPENROUTER_API_KEY="your_key"
```

---

## 🎮 Usage
```bash
python3 app.py
```

## ⌨️ Commands

| Command | Description |
|------|------------|
| /test <file.py> | Autonomous debug & fix |
| /allow write | Enable file editing |
| /log | View recent logs |
| /debug | Toggle debug output |
| /provider <name> | Switch AI provider |
| /scan [path] | List files |
| /read <file> | Load file into context |
| /help | Help menu |

---

## 🐞 Troubleshooting

- **ModuleNotFoundError**: Reinstall dependencies.
- **Ollama Error**: Ensure `ollama serve` is running.
- **Missing Logs**: Create `system.log` manually.

---

## 📂 Folder Structure

```
codevue/
├── aHere is the comprehensive README.md for your project, now officially branded as CodeVue.
It documents the architecture, installation steps for the new agentic features (Ollama/RAG), and the command list we implemented.
File: README.md
# 👁️ CodeVue (NeuroTerm v3.0)

> **The Cyberpunk AI Code Companion.**
> A terminal-based, agentic AI coding environment that remembers your projects, routes tasks intelligently, and autonomously fixes bugs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![AI](https://img.shields.io/badge/AI-Agentic-purple.svg)

---

## 🚀 Overview

CodeVue is not just a wrapper for ChatGPT. It is a fully **Agentic System** that lives in your terminal. It combines local AI (Ollama) for speed and privacy with cloud AI (Gemini/OpenRouter) for complex reasoning.

**Key Capabilities:**
* **🧠 RAG Memory:** Remembers past conversations and code context (using ChromaDB & SQLite).
* **🚦 Smart Routing:** Automatically sends simple tasks to a free local model and complex tasks to paid cloud APIs.
* **🔄 Auto-Fix Loop:** Can run a script, read the error traceback, and apply a fix autonomously until it works.
* **🛡️ Safety First:** Creates timestamped backups before every file edit.
* **📝 Live Logging:** Trace the AI's "thought process" in real-time.

---

## 🏗️ Architecture

CodeVue operates on a **Hybrid Agent Architecture**:

```mermaid
graph TD
    User[User Input] --> Agent[NeuroAgent Executor]
    Agent --> Memory[RAG Memory (ChromaDB)]
    Agent --> Router[NeuroGraph Router (Ollama/Llama 3.2)]
    
    Router -- "Simple Task" --> Local[Local LLM (Ollama)]
    Router -- "Complex Task" --> Cloud[Cloud API (Gemini/OpenRouter)]
    
    Local --> Response
    Cloud --> Response
    
    Response --> UI[Textual TUI]
    Response --> Files[File System]
    
    Files --> Backup[Auto-Backup (SQLite)]

🤖 The Core Stack
 * Frontend: Textual (Modern TUI framework).
 * Orchestration: LangGraph (Decision making).
 * Memory: ChromaDB (Vector Store) + SQLite (Relational Logs).
 * Local Intelligence: Ollama (running llama3.2 & nomic-embed-text).
 * Cloud Intelligence: Google Gemini or OpenRouter.
⚡ Installation
Prerequisites
 * Python 3.10+
 * Ollama installed and running (Download Here).
1. Clone & Setup
git clone [https://github.com/yourusername/codevue.git](https://github.com/yourusername/codevue.git)
cd codevue
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

2. Install Dependencies
pip install -r requirements.txt

3. Pull Local Models
CodeVue requires these two specific models to function:
ollama pull llama3.2       # For Routing & Simple Logic
ollama pull nomic-embed-text  # For RAG Memory

4. Configure Keys
Set your API key for the "Smart" model (optional if you only use local, but recommended).
export GEMINI_API_KEY="your_google_key_here"
# OR
export OPENROUTER_API_KEY="sk-or-..."

🎮 Usage
Start the application:
python3 app.py

⌨️ Commands
| Command | Description |
|---|---|
| /test <file.py> | Autonomous Mode: Runs a script, reads errors, and fixes them in a loop. |
| /allow write | Unlock: Enables file editing permissions (Safety lock is ON by default). |
| /log | View Logs: detailed system logs of the last 20 events. |
| /debug | Debug Mode: Toggles live "thought process" logs in the chat stream. |
| /provider <name> | Switch Brain: Swap between gemini, ollama, or openrouter. |
| /scan [path] | File Explorer: Lists files in the current directory. |
| /read <file> | Context: Reads a file into the chat context. |
| /help | Show the help menu. |
🐞 Troubleshooting
"ModuleNotFoundError"
Run: pip install -r requirements.txt again. Ensure your venv is active.
"Ollama Connection Error"
Ensure Ollama is running in a separate terminal: ollama serve.
"Logs file not found"
The system.log is created on first run. You can manually create it: touch system.log.
📂 Folder Structure
codevue/
├── codevue		   # Global Entry Point (TUI)
├── app.py                 # Main Entry Point (TUI) 
├── update_system.py       # OTA Update Script
├── requirements.txt       # Dependencies
├── system.log             # Live System Logs
├── neuroterm.db           # SQLite History & Backups
├── neuroterm_chroma/      # Vector Database
│
└── core/
    ├── agent.py           # The Orchestrator
    ├── graph.py           # The Router (Brain)
    ├── memory.py          # The Memory (RAG)
    ├── files.py           # File System Tools
    ├── logger.py          # Central Logging
    └── providers/         # API Wrappers
        ├── ollama.py
        ├── gemini.py
        └── openrouter.py

*Global Excecution Setup

 ```
cp -r {project_dir} /usr/local/bin/codevue-files
cp /usr/local/bin/global ../codevue && chmod +x ../codevue

```
*Run from any DIR using "codevue"

Built with 💻 and ☕ by Martin Schoeman.

├──── update_system.py
├── requirements.txt
├── system.log
├── neuroterm.db
├── neuroterm_chroma/
└── core/
    ├── agent.py
    ├── graph.py
    ├── memory.py
    ├── files.py
    ├── logger.py
    └── providers/
        ├── ollama.py
        ├── gemini.py
        └── openrouter.py
```

---
## 🤝 **Contributing**
We love contributors! 🚀
- Fork the repo
- Follow PEP8 for Python code
- Add tests for new features
- Submit PRs with clear descriptions
---
Built with 💻 and ☕ by **Martin Schoeman**
