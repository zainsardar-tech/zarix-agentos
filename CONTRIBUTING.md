# 🤝 Contributing to Zarix AgentOS

Thank you for your interest in contributing to **Zarix AgentOS**! This document outlines the guidelines for contributing.

---

## 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/zarix-agentos.git
   cd zarix-agentos
   ```
3. **Set up** the environment:
   ```bash
   cp .env.example .env
   # Fill in your API keys
   ```
4. **Install** backend dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .  # Install CLI
   ```
5. **Install** frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

---

## 🧑‍💻 Development Workflow

### Running the Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Running the Frontend
```bash
cd frontend
npm run dev
```

### Using the CLI
```bash
zarix info
zarix agents list
zarix llm providers
```

---

## 📝 Code Standards

### Python (Backend)
- Follow **PEP 8** style guidelines
- Use **type hints** on all function signatures
- Add **docstrings** to all public functions and classes
- Keep functions small and focused
- Use `async/await` for I/O operations

### TypeScript (Frontend)
- Use **TypeScript** strict mode
- Prefer **functional components** with hooks
- Use **Tailwind CSS** for styling
- Keep components small and reusable

---

## 🤖 Adding a New Agent

1. Create a new file in `backend/app/agents/` (or add to an existing department file)
2. Define a class inheriting from `BaseAgent`:
   ```python
   class MyAgent(BaseAgent):
       slug = "my_agent"
       name = "My Agent"
       department = "engineering"
       role = "Specialist"
       description = "What this agent does"
       icon = "🔧"
       system_prompt = "You are..."
       skills = ["Skill1", "Skill2"]
       tool_names = ["code_exec"]
       llm_provider = "anthropic"
       llm_model = "claude-sonnet"
   ```
3. Register it in `backend/app/agents/registry.py`
4. Export it in `backend/app/agents/__init__.py`

---

## 🧠 Adding a New LLM Provider

1. Create a new file in `backend/app/llm/`
2. Implement the `BaseLLMProvider` interface (`chat` and `stream_chat`)
3. Register the provider class in `LLMGateway._PROVIDER_CLASSES`
4. Add the API key field to `Settings` in `config.py`
5. Export it in `backend/app/llm/__init__.py`

---

## 🔧 Adding a New Tool

1. Create a new file in `backend/app/tools/`
2. Implement the `BaseTool` interface (`execute` method returning `ToolResult`)
3. Register it in `ToolRegistry._TOOL_CLASSES`
4. Export it in `backend/app/tools/__init__.py`

---

## 📤 Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-amazing-feature
   ```
2. Commit your changes:
   ```bash
   git commit -m "feat: add amazing feature"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/my-amazing-feature
   ```
4. Open a **Pull Request** with a clear description

### Commit Message Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

---

## ✅ Pull Request Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings or errors
- [ ] Tests pass (if applicable)

---

## 🐛 Reporting Bugs

Open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python/Node version)

---

## 💬 Questions & Discussion

Open a [GitHub Discussion](https://github.com/zainsardar-tech/zarix-agentos/discussions) for questions, ideas, and general discussion.

---

Thank you for helping make Zarix AgentOS better! 🚀
