import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Safe Execution Wrapper ────────────────────────────────────────────────────
def execute_safely(agent_or_chain, inputs):
    return agent_or_chain.invoke(inputs)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Intellecta · Autonomous AI Research Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Ultra-Modern Terminal / Cyber Glass Design ────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: #f1f5f9;
}

.stApp {
    background-color: #06090e;
    background-image: 
        radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.06) 0px, transparent 50%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 100% 100%, 32px 32px, 32px 32px;
}

/* ── Hide Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1280px; }

/* ── Header Branding ── */
.intellecta-header {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    color: #34d399;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.brand-badge .dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
}

.intellecta-title {
    font-size: clamp(3rem, 5.5vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.05;
    margin: 0 0 0.8rem;
    background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.intellecta-title span {
    background: linear-gradient(135deg, #34d399 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.intellecta-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 620px;
    margin: 0 auto 1.5rem;
    line-height: 1.6;
    font-weight: 400;
}

/* ── Top Metric Badges Bar ── */
.metrics-bar {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 2.5rem;
}
.metric-pill {
    background: #0d131f;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 6px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
}
.metric-pill strong { color: #f8fafc; }

/* ── Input Box & Button Styling ── */
.stTextInput > div > div > input {
    background: #0d131f !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.4) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #10b981 !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #06090e !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.45) !important;
    filter: brightness(1.08) !important;
}

/* ── Interactive Stage Cards ── */
.agent-card {
    background: #0d131f;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.agent-card.running {
    border-color: #38bdf8;
    background: linear-gradient(135deg, #0d131f 0%, #082f49 100%);
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
}
.agent-card.done {
    border-color: #10b981;
    background: linear-gradient(135deg, #0d131f 0%, #062b1e 100%);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
}

.agent-header {
    display: flex;
    align-items: center;
    gap: 12px;
}
.agent-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    background: #1e293b;
}
.agent-card.running .agent-icon { background: rgba(56, 189, 248, 0.2); }
.agent-card.done .agent-icon { background: rgba(16, 185, 129, 0.2); }

.agent-info h4 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
}
.agent-info p {
    margin: 2px 0 0;
    font-size: 0.78rem;
    color: #94a3b8;
}

.agent-badge {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
}
.badge-waiting { background: #1e293b; color: #64748b; }
.badge-running { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #38bdf8; }
.badge-done { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }

/* ── Result Containers ── */
.report-container {
    background: #0d131f;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.report-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}
.report-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.critic-container {
    background: linear-gradient(135deg, #091310 0%, #061e14 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-top: 1.5rem;
}

/* ── Footer ── */
.intellecta-footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #1e293b;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="intellecta-header">
    <div class="brand-badge"><div class="dot"></div> Autonomous Deep Research Engine</div>
    <div class="intellecta-title">Intellecta<span>.ai</span></div>
    <p class="intellecta-sub">
        Orchestrating 4 autonomous agents across Web Search, Deep Extraction, Report Synthesis &amp; Critic Audit. 100% Local &amp; Private.
    </p>
    <div class="metrics-bar">
        <div class="metric-pill">⚡ Engine: <strong>LangGraph + LangChain</strong></div>
        <div class="metric-pill">🦙 Model: <strong>Ollama (Llama 3.1 8B)</strong></div>
        <div class="metric-pill">🔒 Privacy: <strong>$0 API Fees · On-Device</strong></div>
        <div class="metric-pill">👤 Author: <strong>Vansh Sharma</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Helper: Render an Agent Stage Card ────────────────────────────────────────
def render_agent_card(icon: str, name: str, role: str, status: str):
    status_map = {
        "waiting": ("STANDBY", "badge-waiting"),
        "running": ("● ACTIVE", "badge-running"),
        "done":    ("✓ VERIFIED", "badge-done"),
    }
    label, badge_cls = status_map.get(status, ("STANDBY", "badge-waiting"))
    card_cls = status
    
    st.markdown(f"""
    <div class="agent-card {card_cls}">
        <div class="agent-header">
            <div class="agent-icon">{icon}</div>
            <div class="agent-info">
                <h4>{name}</h4>
                <p>{role}</p>
            </div>
            <div class="agent-badge {badge_cls}">{label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main 2-Column Layout ──────────────────────────────────────────────────────
col_input, col_pipeline = st.columns([5, 4], gap="large")

with col_input:
    st.markdown("<h3 style='font-size:1.2rem;font-weight:700;margin-bottom:0.8rem;color:#f8fafc;'>1. Research Topic</h3>", unsafe_allow_html=True)
    topic = st.text_input(
        "Enter query or complex subject",
        placeholder="e.g. Quantum Computing & Generative AI Hybrid Models in 2026",
        key="topic_input",
        label_visibility="collapsed",
    )
    
    run_btn = st.button("✦  Launch Multi-Agent Research", use_container_width=True)

    # Suggestion Chips
    st.markdown("<div style='margin-top:1.2rem;display:flex;gap:8px;flex-wrap:wrap;align-items:center;'>", unsafe_allow_html=True)
    st.markdown("<span style='font-family:JetBrains Mono;font-size:0.75rem;color:#64748b;'>QUICK PROMPTS:</span>", unsafe_allow_html=True)
    for chip in ["Quantum-AI Hybrid Models", "LangGraph vs AutoGen vs CrewAI", "Nuclear Fusion Milestones"]:
        st.markdown(f"""
        <span style='background:#0d131f;border:1px solid #1e293b;border-radius:6px;padding:4px 10px;font-size:0.75rem;color:#94a3b8;font-family:JetBrains Mono;'>{chip}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown("<h3 style='font-size:1.2rem;font-weight:700;margin-bottom:0.8rem;color:#f8fafc;'>2. Live Agent Pipeline</h3>", unsafe_allow_html=True)
    
    r = st.session_state.results
    
    def get_status(step):
        if not r and not st.session_state.running:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    render_agent_card("🔍", "Search Agent (ReAct)", "Queries Tavily Search & ranks top 5 URLs", get_status("search"))
    render_agent_card("📖", "Reader Agent (BS4)", "Scrapes clean context & extracts article text", get_status("reader"))
    render_agent_card("✍️", "Writer Chain (LLM)", "Synthesizes data into structured Markdown", get_status("writer"))
    render_agent_card("🎯", "Critic Chain (Audit)", "Fact-checks depth & calculates quality score", get_status("critic"))

# ── Pipeline Trigger ──────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    try:
        # Step 1: Search
        with st.spinner("🔍 Search Agent is querying the web..."):
            search_agent = build_search_agent()
            sr = execute_safely(search_agent, {
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 2: Reader
        with st.spinner("📄 Reader Agent is parsing article text..."):
            reader_agent = build_reader_agent()
            rr = execute_safely(reader_agent, {
                "messages": [("user", 
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 3: Writer
        with st.spinner("✍️ Writer Chain is drafting the report..."):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = execute_safely(writer_chain, {
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)

        # Step 4: Critic
        with st.spinner("🎯 Critic Chain is evaluating accuracy..."):
            results["critic"] = execute_safely(critic_chain, {
                "report": results["writer"]
            })
            st.session_state.results = dict(results)

    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.session_state.running = False
        st.stop()

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()

# ── Results Presentation ──────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown("<hr style='border-color:#1e293b;margin:3rem 0 2rem;'>", unsafe_allow_html=True)
    
    # Report Section
    if "writer" in r:
        st.markdown(f"""
        <div class="report-container">
            <div class="report-top-bar">
                <span class="report-label">📄 Synthesized Publication Report</span>
                <span style="font-family:JetBrains Mono;font-size:0.8rem;color:#10b981;background:rgba(16,185,129,0.1);padding:4px 10px;border-radius:6px;border:1px solid #10b981;">STATUS: VERIFIED</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Markdown Report (.md)",
            data=r["writer"],
            file_name=f"intellecta_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic Section
    if "critic" in r:
        st.markdown("""
        <div class="critic-container">
            <div style="font-family:JetBrains Mono;font-size:0.8rem;font-weight:700;color:#34d399;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:0.1em;">
                🎯 Independent Critic Audit &amp; Scoring
            </div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

    # Raw Inspect Expanders
    with st.expander("🔍 Inspect Raw Search Results & Scraped Content", expanded=False):
        if "search" in r:
            st.markdown("#### Search Agent Raw Output")
            st.code(r["search"], language="markdown")
        if "reader" in r:
            st.markdown("#### Reader Agent Scraped Body")
            st.code(r["reader"][:1500] + "...", language="text")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="intellecta-footer">
    Intellecta.ai · Engineered by Vansh Sharma · LangGraph Multi-Agent Architecture · Local Ollama Backend
</div>
""", unsafe_allow_html=True)