# Architecture Overview

## System Design

Intellecta follows a **pipeline architecture** with four specialized agents connected via LangGraph state management.

```mermaid
graph LR
    A[User Query] --> B[Search Agent]
    B --> C[Reader Agent]
    C --> D[Writer Chain]
    D --> E[Critic Chain]
    E --> F[Final Report]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#fff3e0
    style F fill:#e0f2f1
```

## State Management

LangGraph maintains a typed state object passed between agents:

```python
class ResearchState(TypedDict):
    query: str
    search_results: List[SearchResult]
    scraped_content: List[ScrapedContent]
    draft_report: str
    critic_feedback: CriticFeedback
    final_report: str
    iteration: int
```

## Agent Details

### 1. Search Agent (React Agent)
- **Tool**: Tavily Search API
- **Output**: Top 5 relevant URLs with snippets
- **Config**: Recency, domain filtering, result count

### 2. Reader Agent (React Agent)
- **Tool**: Web scraping (requests + BeautifulSoup)
- **Output**: Cleaned content (max 3000 chars per source)
- **Config**: Timeout, user-agent, content selectors

### 3. Writer Chain (LLM Chain)
- **Model**: Ollama (Llama 3.1)
- **Prompt**: Structured report generation with citations
- **Output**: Markdown report

### 4. Critic Chain (LLM Chain)
- **Model**: Ollama (Llama 3.1)
- **Prompt**: Quality evaluation rubric
- **Output**: Score (1-10), strengths, improvements