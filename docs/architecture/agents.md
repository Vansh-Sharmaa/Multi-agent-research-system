# Agents

## Search Agent

**File:** `agents.py` → `create_search_agent()`

### Purpose
Locates the most relevant web resources for a research query.

### Implementation
```python
def create_search_agent() -> AgentExecutor:
    tools = [TavilySearchResults(max_results=5)]
    prompt = ChatPromptTemplate.from_messages([
        ("system", SEARCH_SYSTEM_PROMPT),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### Configuration
| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_results` | 5 | Number of search results |
| `search_depth` | "basic" | "basic" or "advanced" |
| `include_domains` | [] | Restrict to specific domains |
| `exclude_domains` | [] | Exclude specific domains |

### Output Format
```json
[
  {
    "url": "https://example.com",
    "title": "Page Title",
    "content": "Relevant snippet...",
    "score": 0.95
  }
]
```

---

## Reader Agent

**File:** `agents.py` → `create_reader_agent()`

### Purpose
Deep-scrapes and extracts core content from selected URLs.

### Implementation
```python
def create_reader_agent() -> AgentExecutor:
    tools = [ScrapeWebsiteTool()]
    prompt = ChatPromptTemplate.from_messages([
        ("system", READER_SYSTEM_PROMPT),
        ("human", "{urls}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### Scraping Strategy
1. Fetch HTML with requests (browser headers)
2. Parse with BeautifulSoup
3. Extract main content (remove nav, footer, ads)
4. Clean: remove scripts, styles, extra whitespace
5. Truncate to 3000 characters

### Output Format
```json
[
  {
    "url": "https://example.com",
    "title": "Page Title",
    "content": "Full extracted content...",
    "word_count": 1250
  }
]
```

---

## Writer Chain

**File:** `agents.py` → `create_writer_chain()`

### Purpose
Synthesizes research findings into a structured markdown report.

### Prompt Template
```
You are an expert research analyst. Create a comprehensive report from the provided sources.

Structure:
1. Executive Summary
2. Detailed Analysis (with citations)
3. Key Insights
4. Sources

Cite sources as [1], [2], etc. referencing the source list.
```

### Output
Structured markdown report with proper citations.

---

## Critic Chain

**File:** `agents.py` → `create_critic_chain()`

### Purpose
Evaluates report quality and provides structured feedback.

### Evaluation Rubric
| Criterion | Weight |
|-----------|--------|
| Accuracy | 30% |
| Depth | 25% |
| Clarity | 20% |
| Citation Quality | 15% |
| Structure | 10% |

### Output Format
```json
{
  "score": 8.5,
  "strengths": ["Well-cited", "Comprehensive coverage"],
  "improvements": ["Add more recent sources", "Deepen technical analysis"],
  "pass": true
}
```