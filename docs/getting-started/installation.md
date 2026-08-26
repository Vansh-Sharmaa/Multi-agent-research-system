# Installation

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running
- Llama 3.1 model: `ollama pull llama3.1:8b`
- [Tavily API Key](https://tavily.com/) (free tier available)

## Install from Source

```bash
# Clone the repository
git clone https://github.com/Vansh-Sharmaa/Multi-agent-research-system.git
cd Multi-agent-research-system

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

## Verify Installation

```bash
# Check Ollama is running
ollama list

# Run a quick test
python pipeline.py "test query" --max-steps 1
```

## Docker Installation

```bash
# Pull pre-built image
docker pull vanshsharmaa/intellecta-multi-agent:latest

# Or build locally
docker build -t intellecta-multi-agent .

# Run
docker run -p 8501:8501 \
  -e TAVILY_API_KEY=your_key \
  -v ~/.ollama:/root/.ollama \
  intellecta-multi-agent
```