import streamlit as st
import time
from pipeline import run_research_pipeline

# Page config
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0a0a0f; }
    .stApp { background-color: #0a0a0f; }

    .title-text {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle-text {
        text-align: center;
        color: #7a7a8e;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .step-card {
        background: #111118;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .step-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-text">🧠 Multi-Agent Research System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Powered by Mistral AI · Search → Read → Write → Critique</div>', unsafe_allow_html=True)

st.divider()

# Input
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Impact of war on stock market...",
        label_visibility="collapsed"
    )
    run_btn = st.button("🚀 Generate Research Report", use_container_width=True, type="primary")

st.divider()

# Run pipeline
if run_btn and topic.strip():

    # Step indicators
    st.markdown("### ⚙️ Pipeline Running...")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        s1 = st.status("🔍 Search Agent", expanded=False)
    with col_s2:
        s2 = st.status("📄 Reader Agent", expanded=False)
    with col_s3:
        s3 = st.status("✍️ Writer", expanded=False)
    with col_s4:
        s4 = st.status("🧠 Critic", expanded=False)

    state = {}

    # ── Step 1: Search
    s1.update(label="🔍 Search Agent — Running...", state="running")
    try:
        from agents import build_search_agent
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result['messages'][-1].content
        s1.update(label="🔍 Search Agent — Done ✅", state="complete")
    except Exception as e:
        s1.update(label=f"🔍 Search Agent — Failed ❌", state="error")
        st.error(f"Search Agent Error: {e}")
        st.stop()

    time.sleep(6)

    # ── Step 2: Reader
    s2.update(label="📄 Reader Agent — Running...", state="running")
    try:
        from agents import build_reader_agent
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result['messages'][-1].content
        s2.update(label="📄 Reader Agent — Done ✅", state="complete")
    except Exception as e:
        s2.update(label="📄 Reader Agent — Failed ❌", state="error")
        st.error(f"Reader Agent Error: {e}")
        st.stop()

    time.sleep(6)

    # ── Step 3: Writer
    s3.update(label="✍️ Writer — Running...", state="running")
    try:
        from agents import writer_chain
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        s3.update(label="✍️ Writer — Done ✅", state="complete")
    except Exception as e:
        s3.update(label="✍️ Writer — Failed ❌", state="error")
        st.error(f"Writer Error: {e}")
        st.stop()

    time.sleep(6)

    # ── Step 4: Critic
    s4.update(label="🧠 Critic — Running...", state="running")
    try:
        from agents import critic_chain
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })
        s4.update(label="🧠 Critic — Done ✅", state="complete")
    except Exception as e:
        s4.update(label="🧠 Critic — Failed ❌", state="error")
        st.error(f"Critic Error: {e}")
        st.stop()

    st.success("✅ Research pipeline completed successfully!")
    st.divider()

    # ── Results
    st.markdown("## 📋 Results")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Final Report",
        "🧠 Critic Feedback",
        "🔍 Search Results",
        "📄 Scraped Content"
    ])

    with tab1:
        st.markdown(f"### Research Report: *{topic}*")
        st.markdown(state["report"])
        st.download_button(
            label="⬇️ Download Report",
            data=state["report"],
            file_name=f"report_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown"
        )

    with tab2:
        st.markdown("### Critic's Evaluation")
        st.markdown(state["feedback"])

    with tab3:
        st.markdown("### Raw Search Results")
        st.markdown(state["search_results"])

    with tab4:
        st.markdown("### Scraped Web Content")
        st.markdown(state["scraped_content"])

elif run_btn and not topic.strip():
    st.warning("⚠️ Please enter a research topic.")