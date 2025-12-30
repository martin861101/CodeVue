# 🎉 **NeuroTerm: Your AI-Powered Code Companion**
> *Where AI meets your codebase – fixing bugs, writing code, and having fun while doing it!*

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![AI](https://img.shields.io/badge/AI--Powered-Yes-green) ![License](https://img.shields.io/badge/License-MIT-orange)

---

## 🚀 **Quick Start – Get Coding in 5 Minutes!**

### Prerequisites
- Python 3.8+ 🐍
- API keys for your favorite AI providers 🤖

### Installation
```bash
pip install neuroterm  # Coming soon to PyPI!
# Or clone and run:
git clone https://github.com/your-repo/neuroterm
cd neuroterm && pip install -r requirements.txt
```

### First Steps
1. Set up your API keys (see below)
2. `python app.py`
3. Type `/help` and start chatting! 💬

---

## 🛠️ **Command Reference – Your AI Toolbox**

### 📁 **File Operations**
| Command | Description | Example |
|---------|-------------|---------|
| `/read <file>` | Peek into any file 📖 | `/read app.py` |
| `/write <file> <content>` | Edit files safely ✏️ | `/write hello.py print("Hello!")` |
| `/scan [path]` | Explore directories 🔍 | `/scan src/` |
| `/tree [path]` | See folder structure 🌳 | `/tree .` |
| `/exec <file>` | Run Python scripts ⚡ | `/exec test.py` |
| `/new project <name>` | Bootstrap new projects 🏗️ | `/new project myapp` |

### 🤖 **AI Integration**
| Command | Description | Example |
|---------|-------------|---------|
| *Direct chat* | Talk to AI about anything 💭 | "How do I fix this bug?" |
| `/provider <name>` | Switch AI providers 🔄 | `/provider gemini` |
| `/model <name>` | Change AI models 🎭 | `/model gpt-4` |

### 🔒 **Safety & Permissions**
| Command | Description | Example |
|---------|-------------|---------|
| `/allow write` | Enable file editing ✅ | `/allow write` |
| `/deny write` | Lock down writes 🚫 | `/deny write` |
| `/open <file>` | Set context file 📌 | `/open main.py` |
| `/clear` | Fresh start 🧹 | `/clear` |

### 🔮 **Planned Features** (Coming Soon!)
- `/autofix <file>` – Auto-magic code fixing ✨
- `/revert <file>` – Time travel back to safety ⏪

---

## 🎯 **Key Features – Why NeuroTerm Rocks**

- **🧠 AI-Powered**: Chat with intelligent assistants about your code
- **📂 Safe File Ops**: Read, write, and execute with permission controls
- **🔄 Multi-Provider**: Gemini, Ollama, OpenRouter – pick your AI!
- **🏗️ Project Gen**: Scaffold new projects instantly
- **🔐 Secure**: Backups, permissions, and safety first
- **⚡ Fast**: Stream responses for smooth coding sessions

---

## 🔑 **API Setup – Unlock the Power**

### Google Gemini 🤖
```bash
export GEMINI_API_KEY="your_key_here"
# Get from: https://makersuite.google.com/app/apikey
```

### Ollama 🏠
```bash
# Install Ollama locally
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3  # or your favorite model
# No API key needed – runs locally!
```

### OpenRouter 🌐
```bash
export OPENROUTER_API_KEY="your_key_here"
# Get from: https://openrouter.ai/keys
# Supports 100+ models from various providers
```

*Pro tip: Store keys in `.env` file for easy management!*

---

## 📚 **Usage Examples – See It In Action**

### Basic Chat
```
You: How do I reverse a string in Python?
Neuroterm: Here's a simple way: `s[::-1]` ✨
```

### File Workflow
```
/read buggy.py
# AI analyzes and suggests fixes
/write buggy.py [fixed code]
/exec buggy.py  # Test it works!
```

### Project Setup
```
/new project mywebapp
/scan mywebapp/  # See the structure
/write mywebapp/app.py [your code here]
```

---

## ⚙️ **Advanced Usage & Integrations**

### Custom Workflows
- **Code Review**: `/read file.py` then "Review this code for issues"
- **Refactoring**: "Refactor this function to be more efficient"
- **Testing**: Generate and run tests with `/exec test_script.py`

### Integrations
- **Git Integration**: Commit changes with AI-generated messages
- **IDE Plugins**: Planned for VS Code, PyCharm
- **CI/CD**: Auto-fix in pipelines (future feature)

### Configuration
- Environment variables for API keys
- Supported file types: .py, .js, .html, .css, .json, .md
- Safety settings: Write permissions, file size limits

---

## 🛡️ **Safety & Security**

- **Write Permissions**: Must explicitly enable with `/allow write`
- **Backups**: Automatic `.backup` files before changes
- **Access Control**: Files outside project root blocked
- **Rate Limiting**: Respects API provider limits
- **Data Privacy**: No code sent to external servers (except API calls)

---

## 🐛 **Troubleshooting**

### Common Issues
- **"Provider not found"**: Check API key setup
- **"Permission denied"**: Run `/allow write`
- **"File not found"**: Use `/scan` to verify paths
- **Slow responses**: Try different provider or model

### Performance Tips
- Use local Ollama for fastest responses
- Keep files under 100KB for best performance
- Close app between sessions to free memory

---

## 🤝 **Contributing**

We love contributors! 🚀
- Fork the repo
- Follow PEP8 for Python code
- Add tests for new features
- Submit PRs with clear descriptions

---

## 📄 **License**

MIT License - See LICENSE file for details.