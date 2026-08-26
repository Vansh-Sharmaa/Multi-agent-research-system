# Contributing to Intellecta

Thank you for your interest in contributing! This document outlines the process for contributing to the Multi-Agent Research System.

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/Vansh-Sharmaa/Multi-agent-research-system/issues)
2. Create new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Ollama version)
   - Logs/screenshots if applicable

### Suggesting Features

1. Open a [feature request issue](https://github.com/Vansh-Sharmaa/Multi-agent-research-system/issues/new)
2. Describe the feature and use case
3. Explain why it would be valuable

### Pull Request Process

1. **Fork** the repository
2. **Create branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** following code style
4. **Test** your changes: `pytest`
5. **Lint**: `ruff check . && black --check . && isort --check-only .`
6. **Commit**: `git commit -m 'feat: your feature description'`
7. **Push**: `git push origin feature/your-feature-name`
8. **Open PR** against `main` branch

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Multi-agent-research-system.git
cd Multi-agent-research-system

# Add upstream remote
git remote add upstream https://github.com/Vansh-Sharmaa/Multi-agent-research-system.git

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

- **Formatter**: Black (line length 88)
- **Import Sort**: isort (profile: black)
- **Linter**: Ruff
- **Types**: MyPy (strict mode)

Run all checks:
```bash
ruff check . --fix
black .
isort .
mypy .
pytest --cov=.
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

Examples:
```
feat: add support for Groq LLM provider
fix: handle Tavily API rate limiting
docs: update installation guide for Windows
refactor: simplify agent state management
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_agents.py -v

# Watch mode (requires pytest-watch)
ptw
```

## Architecture Guidelines

- Keep agents focused and single-purpose
- Use LangGraph for state management
- Prefer composition over inheritance
- Document public APIs with docstrings
- Add type hints to all functions

## Release Process

Maintainers only:
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions creates release automatically

## Questions?

Open a [discussion](https://github.com/Vansh-Sharmaa/Multi-agent-research-system/discussions) or email engagevansh@gmail.com