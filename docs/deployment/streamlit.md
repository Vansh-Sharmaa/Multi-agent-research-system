# Streamlit Cloud Deployment

## Overview

Deploy Intellecta to [Streamlit Community Cloud](https://streamlit.io/cloud) for free hosting with automatic GitHub integration.

## Prerequisites

1. GitHub repository (this one)
2. Streamlit account (free at [share.streamlit.io](https://share.streamlit.io))
3. Tavily API key

## Deployment Steps

### 1. Push to GitHub

Ensure your code is on the `main` branch:

```bash
git add .
git commit -m "feat: prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Create Streamlit App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect GitHub account
4. Select repository: `Vansh-Sharmaa/Multi-agent-research-system`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **"Deploy!"**

### 3. Configure Secrets

In Streamlit Cloud dashboard:

1. Go to your app → **Settings** → **Secrets**
2. Add secrets in TOML format:

```toml
TAVILY_API_KEY = "your_tavily_api_key_here"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"
```

**Note:** Streamlit Cloud doesn't support Ollama directly. For cloud deployment, you'll need to use a cloud LLM provider (Groq, OpenAI, Anthropic) instead of Ollama.

## Using Cloud LLMs (Required for Streamlit Cloud)

Since Streamlit Cloud doesn't support local Ollama, modify `agents.py` to use a cloud provider:

```python
# Option 1: Groq (Fast, free tier)
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# Option 2: OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

# Option 3: Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=os.getenv("ANTHROPIC_API_KEY"))
```

Add the API key to Streamlit Secrets:
```toml
GROQ_API_KEY = "your_groq_key"
# or
OPENAI_API_KEY = "your_openai_key"
```

## Automatic Deployment

The GitHub Actions workflow (`.github/workflows/ci.yml`) can auto-deploy on push to main:

1. Get deploy hook from Streamlit Cloud:
   - App settings → **Deploy hook** → Copy URL
2. Add to GitHub repository secrets:
   - Settings → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `STREAMLIT_DEPLOY_HOOK`
   - Value: (paste deploy hook URL)

Now every push to `main` triggers auto-deploy.

## Custom Domain

1. In Streamlit Cloud: App settings → **Custom domain**
2. Add CNAME record: `your-app.yourdomain.com` → `your-app.streamlit.app`
3. Enable HTTPS (automatic via Let's Encrypt)

## Monitoring

- **Logs**: Streamlit Cloud dashboard → **Manage app** → **View logs**
- **Analytics**: Built-in viewer stats
- **Uptime**: 99.9% SLA on Community Cloud

## Limitations

| Limitation | Workaround |
|------------|------------|
| No local Ollama | Use Groq/OpenAI/Anthropic API |
| 1 GB RAM limit | Optimize model size, use quantization |
| No GPU | Use CPU-optimized models |
| Sleep after inactivity | Upgrade to paid plan or use cron ping |

## Alternative: Hugging Face Spaces

For GPU support, deploy to [Hugging Face Spaces](https://huggingface.co/spaces):

```bash
# Create Space on HF Hub
# Select "Streamlit" SDK
# Push code to Space repo
```

HF Spaces offers free CPU and paid GPU tiers.