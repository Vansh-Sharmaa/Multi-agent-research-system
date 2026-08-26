# Quick Start

## Run the Web UI (Recommended)

```bash
# Start Ollama (in separate terminal)
ollama serve

# Start Streamlit app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Run from CLI

```bash
# Quick research
python pipeline.py "Impact of AI on healthcare"

# With options
python pipeline.py "Quantum computing cryptography" \
  --model llama3.1:8b \
  --max-results 5 \
  --output report.md
```

## Example Queries

Try these research topics:

- `"Latest developments in quantum error correction"`
- `"Impact of transformer architecture on NLP"`
- `"Sustainable energy storage technologies 2024"`
- `"Multi-agent AI systems architecture patterns"`
- `"Fine-tuning LLMs with QLoRA best practices"`

## Understanding the Output

The system produces a structured markdown report with:

1. **Executive Summary** — High-level findings
2. **Detailed Analysis** — Technical deep-dive with citations
3. **Key Insights** — Most important takeaways
4. **Sources** — All referenced URLs
5. **Critic Score** — Quality assessment (1-10)

## Next Steps

- [Configuration](configuration.md) — Customize models, agents, search
- [Architecture Overview](../architecture/overview.md) — Understand the system design
- [Deployment](../deployment/docker.md) — Production deployment options