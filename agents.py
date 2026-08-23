from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.rate_limiters import InMemoryRateLimiter 
from tools import web_search , scrape_url 
from dotenv import load_dotenv
import os

load_dotenv()

# --- RATE LIMITER SETUP ---
# 0.2 requests per second = 1 request every 5 seconds. 
# This keeps you safely at 12 Requests Per Minute (RPM), below the 15 RPM free tier limit.
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.2,  
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)

# --- MODEL SETUP ---
# Explicit base_url and keep_alive to maintain stable local connection on Windows
llm = ChatOllama(
    model="llama3.1", 
    base_url="http://127.0.0.1:11434",
    temperature=0,
    keep_alive="10m"
)


#1st agent 
def build_search_agent():
    return create_react_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 
def build_reader_agent():
    return create_react_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()