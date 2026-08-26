# API Reference

## Pipeline Module

### `run_pipeline(query: str, **kwargs) -> ResearchState`
Execute the full research pipeline.

**Parameters:**
- `query` (str): Research question
- `model` (str, optional): Ollama model name
- `max_results` (int, optional): Search results count
- `max_iterations` (int, optional): Critic revision loops

**Returns:** `ResearchState` with `final_report`, `critic_feedback`, `sources`

---

## Agents Module

### `create_search_agent(config: SearchConfig) -> AgentExecutor`
Creates the web search agent.

**Config:**
```python
@dataclass
class SearchConfig:
    max_results: int = 5
    search_depth: str = "basic"
    include_domains: List[str] = field(default_factory=list)
    exclude_domains: List[str] = field(default_factory=list)
```

### `create_reader_agent(config: ReaderConfig) -> AgentExecutor`
Creates the content extraction agent.

**Config:**
```python
@dataclass
class ReaderConfig:
    max_chars: int = 3000
    timeout: int = 30
    user_agent: str = "Mozilla/5.0..."
```

### `create_writer_chain(config: WriterConfig) -> Runnable`
Creates the report generation chain.

### `create_critic_chain(config: CriticConfig) -> Runnable`
Creates the quality evaluation chain.

---

## Tools Module

### `TavilySearchResults(max_results: int) -> Tool`
LangChain tool for Tavily web search.

### `ScrapeWebsiteTool() -> Tool`
LangChain tool for web scraping.

**Methods:**
- `scrape(url: str) -> ScrapedContent`
- `scrape_batch(urls: List[str]) -> List[ScrapedContent]`

---

## Models

### `ResearchState` (TypedDict)
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

### `SearchResult`
```python
@dataclass
class SearchResult:
    url: str
    title: str
    content: str
    score: float
```

### `ScrapedContent`
```python
@dataclass
class ScrapedContent:
    url: str
    title: str
    content: str
    word_count: int
```

### `CriticFeedback`
```python
@dataclass
class CriticFeedback:
    score: float
    strengths: List[str]
    improvements: List[str]
    pass: bool
```

---

## CLI

### `pipeline.py`
```bash
python pipeline.py "query" [options]

Options:
  --model MODEL          Ollama model (default: llama3.1:8b)
  --max-results N        Search results (default: 5)
  --max-iterations N     Critic loops (default: 2)
  --output FILE          Save report to file
  --verbose              Enable debug logging
```

### `app.py` (Streamlit)
```bash
streamlit run app.py [--server.port PORT] [--server.address ADDR]
```