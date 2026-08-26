# Configuration

## Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TAVILY_API_KEY` | Tavily Search API key | `tvly-xxx` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model to use | `llama3.1:8b` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Streamlit port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Streamlit bind address | `0.0.0.0` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Model Configuration

Intellecta uses Ollama for local LLM inference. Supported models:

```bash
# Recommended (8B params, good quality/speed balance)
ollama pull llama3.1:8b

# Higher quality (70B params, slower)
ollama pull llama3.1:70b

# Faster (3B params)
ollama pull llama3.2:3b
```

Update `OLLAMA_MODEL` in `.env` to switch models.

## Agent Configuration

Agent behavior can be customized in `agents.py`:

- **Search Agent**: Number of results, search depth, recency
- **Reader Agent**: Max characters to extract, timeout
- **Writer Chain**: Report style, length, structure
- **Critic Chain**: Scoring criteria, strictness