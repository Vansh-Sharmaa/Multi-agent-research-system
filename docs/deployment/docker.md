# Docker Deployment

## Quick Start

```bash
# Build image
docker build -t intellecta-multi-agent .

# Run container
docker run -d \
  --name intellecta \
  -p 8501:8501 \
  -p 11434:11434 \
  -e TAVILY_API_KEY=your_key \
  -v ~/.ollama:/root/.ollama \
  intellecta-multi-agent
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  intellecta:
    build: .
    ports:
      - "8501:8501"
      - "11434:11434"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - OLLAMA_MODEL=llama3.1:8b
    volumes:
      - ~/.ollama:/root/.ollama
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

Run with:
```bash
docker-compose up -d
```

## Production Considerations

### Resource Requirements
| Component | CPU | RAM | GPU |
|-----------|-----|-----|-----|
| Ollama (8B) | 4+ cores | 8 GB | Optional (CUDA) |
| Streamlit | 1 core | 1 GB | No |
| **Total** | **4+ cores** | **9+ GB** | **Optional** |

### Environment Variables
```yaml
environment:
  - TAVILY_API_KEY=${TAVILY_API_KEY}
  - OLLAMA_BASE_URL=http://localhost:11434
  - OLLAMA_MODEL=llama3.1:8b
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - LOG_LEVEL=INFO
```

### Persistent Volumes
```yaml
volumes:
  - ollama_data:/root/.ollama      # Model cache
  - app_data:/app/data             # Reports, logs
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

## Multi-Architecture Build

```bash
# Build for AMD64 and ARM64
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t vanshsharmaa/intellecta-multi-agent:latest \
  --push .
```

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
1. Builds and tests the Docker image
2. Pushes to Docker Hub on main branch
3. Deploys to Streamlit Cloud (if configured)

### Required Secrets
| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `STREAMLIT_DEPLOY_HOOK` | Streamlit Cloud deploy webhook |