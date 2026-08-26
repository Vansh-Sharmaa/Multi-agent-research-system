# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-27

### Added
- Initial release of Intellecta: Autonomous Multi-Agent Research Engine
- Four-agent pipeline: Search Agent, Reader Agent, Writer Chain, Critic Chain
- LangGraph-based stateful orchestration
- Local-first LLM backend via Ollama (Llama 3.1 8B)
- Glassmorphism Streamlit UI with real-time stage cards
- CLI alternative (`pipeline.py`) for command-line research
- Tavily API integration for web search
- Self-reflecting quality control via Critic agent
- Comprehensive documentation and architecture diagrams
- Docker support for containerized deployment
- CI/CD pipeline with linting, testing, security scanning

### Technical Details
- **Agents**: 4 specialized agents (React Agent + LLM Chains)
- **Framework**: LangGraph + LangChain (LCEL)
- **LLM**: Ollama (llama3.1:8b)
- **Search**: Tavily API
- **UI**: Streamlit with custom CSS/JS
- **Python**: 3.11+

---

## [Unreleased]

### Planned
- [ ] Multi-model support (Llama 3.2, Mistral, Gemma)
- [ ] Export reports to PDF/Notion/Google Docs
- [ ] Scheduled/recurring research jobs
- [ ] Team collaboration features
- [ ] Plugin system for custom agents
- [ ] Webhook integrations (Slack, Discord, Email)
- [ ] Research history & versioning
- [ ] Advanced filtering & source credibility scoring