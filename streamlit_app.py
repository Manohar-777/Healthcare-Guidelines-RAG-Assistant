"""
Streamlit UI for Healthcare Guidelines RAG Assistant
Professional interface showing full retrieval pipeline and sources
"""

import streamlit as st
import requests
import json
from datetime import datetime

import os
API_URL = os.getenv("API_URL", "http://localhost:9070")

# Page config
st.set_page_config(
    page_title="Healthcare Guidelines Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Answer box */
    .answer-box {
        background-color: #e8f4f8;
        border-left: 5px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;  /* FIXED: Dark text */
    }
    
    /* Passage box - FIXED */
    .passage-box {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .passage-header {
        background-color: #495057;  /* Darker background */
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .passage-text {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #6c757d;
        color: #212529;  /* FIXED: Dark text */
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Citation box - FIXED */
    .citation-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        color: #333;  /* FIXED: Dark text */
    }
    
    /* Confidence indicators */
    .confidence-high {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .confidence-medium {
        color: #fd7e14;  /* Changed to orange */
        font-weight: bold;
        font-size: 1.2rem;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Metrics boxes - FIXED SIZE */
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #ddd;
        min-height: 100px;  /* FIXED: Same height for all */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Status badges - FIXED */
    .status-validated {
        background-color: #28a745;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        font-size: 1rem;
    }
    .status-review {
        background-color: #ffc107;
        color: #333;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'question_text' not in st.session_state:
    st.session_state.question_text = ""

# Header
st.markdown('<div class="main-header">🏥 Healthcare Guidelines RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Evidence-based answers from WHO, CDC, and NIH guidelines with full source transparency</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ System Controls")
    
    # API connection check
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
            system_info = response.json()
            
            with st.expander("📊 System Information", expanded=False):
                st.metric("Version", system_info.get('version', 'N/A'))
                st.metric("Indexed Chunks", system_info.get('num_chunks', 'N/A'))
                st.metric("Documents", "69 guidelines")
                st.write(f"**LLM:** Groq Llama 3.1 8B")
                st.write(f"**Embeddings:** all-MiniLM-L6-v2")
                
                st.divider()
                st.write("**Performance:**")
                st.write("• Precision@5: 93.3%")
                st.write("• Validation Rate: 76%")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Not Running")
        st.info("💡 **Start server:**\n```\nuvicorn app.server:app --port 9070\n```")
    
    st.divider()
    
    # Query settings
    st.subheader("🎛️ Query Settings")
    top_k = st.slider("Sources to retrieve", 1, 10, 5, help="Number of guideline sections to search")
    use_llm = st.checkbox("🤖 Use AI Generation", value=True, 
                          help="Enable LLM for natural language answers")
    show_raw = st.checkbox("📄 Show Full Passages", value=True,
                          help="Display complete text from retrieved sources")
    
    st.divider()
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    if st.button("🔄 Clear All", use_container_width=True):
        st.session_state.history = []
        st.session_state.current_result = None
        st.session_state.question_text = ""
        st.rerun()

# Sample Questions Section
st.markdown("---")
st.subheader("💡 Try These Sample Questions (Click to Use)")

sample_questions = [
    {
        "q": "When should hand hygiene be performed?",
        "icon": "🧼",
        "category": "Hand Hygiene"
    },
    {
        "q": "How should PPE be selected based on exposure risk?",
        "icon": "🦺",
        "category": "PPE Selection"
    },
    {
        "q": "What are the principles of WHO environmental cleaning guidelines?",
        "icon": "🧹",
        "category": "Environmental"
    },
    {
        "q": "When can symptomatic healthcare staff return to work?",
        "icon": "👨‍⚕️",
        "category": "Return to Work"
    },
    {
        "q": "What is the hierarchy of clinical evidence?",
        "icon": "📊",
        "category": "Evidence"
    },
    {
        "q": "What practices are included in respiratory etiquette?",
        "icon": "😷",
        "category": "Respiratory"
    }
]

# Display sample questions in a nice grid
cols = st.columns(3)
for idx, sample in enumerate(sample_questions):
    with cols[idx % 3]:
       
        if st.button(
            f"{sample['icon']} {sample['category']}", 
            key=f"sample_{idx}",
            use_container_width=True,
            help=f"Click to ask: {sample['q']}"
        ):
            # Set the question and trigger query
            st.session_state.question_text = sample['q']
            st.session_state.trigger_query = True
            st.rerun()

st.markdown("---")

# Main query interface
st.subheader("🔍 Ask Your Question")

# Question input - use session state
question = st.text_area(
    "Enter your healthcare guideline question:",
    value=st.session_state.question_text,
    height=100,
    placeholder="e.g., What are the key principles of hand hygiene according to WHO?",
    key="question_input_box"
)

# Update session state when text changes
if question != st.session_state.question_text:
    st.session_state.question_text = question

# Submit button
col1, col2 = st.columns([3, 1])
with col1:
    submit = st.button("🚀 Get Answer", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Clear", use_container_width=True):
        st.session_state.question_text = ""
        st.session_state.current_result = None
        st.rerun()

# Check if we should trigger query (from sample question click)
if hasattr(st.session_state, 'trigger_query') and st.session_state.trigger_query:
    submit = True
    st.session_state.trigger_query = False

# Process query
if submit and st.session_state.question_text.strip():
    with st.spinner("🔎 Searching guidelines and generating answer..."):
        try:
            payload = {
                "question": st.session_state.question_text,
                "top_k": top_k,
                "use_llm": use_llm
            }
            
            response = requests.post(
                f"{API_URL}/qa",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.current_result = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": st.session_state.question_text,
                    "result": result,
                    "settings": {
                        "top_k": top_k,
                        "use_llm": use_llm
                    }
                }
                
                # Add to history
                st.session_state.history.insert(0, st.session_state.current_result)
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.code(response.text)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display current result
if st.session_state.current_result:
    result_data = st.session_state.current_result
    result = result_data["result"]
    
    st.markdown("---")
    st.success("✅ Answer Generated Successfully")
    
    # Answer Section
    st.markdown("### 💡 Generated Answer")
    answer = result.get("answer", "No answer generated")
    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
    
    # Metadata row - FIXED BOX SIZES
    st.markdown("### 📊 Answer Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    confidence = result.get("confidence", 0)
    status = result.get("status", "unknown")
    method = result.get("generation_method", "unknown")
    num_citations = len(result.get("citations", []))
    
    with col1:
        conf_class = "confidence-high" if confidence >= 0.7 else "confidence-medium" if confidence >= 0.4 else "confidence-low"
        st.markdown(f'<div class="metric-box"><div class="metric-value {conf_class}">{confidence:.1%}</div><div class="metric-label">Confidence Score</div></div>', unsafe_allow_html=True)
    
    with col2:
        status_class = "status-validated" if status == "validated" else "status-review"
        status_text = status.replace("_", " ").upper()
        st.markdown(f'<div class="metric-box"><div class="metric-value"><span class="{status_class}">{status_text}</span></div><div class="metric-label">Validation Status</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="metric-box"><div class="metric-value" style="font-size: 1.3rem;">{method.upper()}</div><div class="metric-label">Generation Method</div></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{num_citations}</div><div class="metric-label">Sources Cited</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Citations Section
    st.markdown("### 📚 Source Citations")
    citations = result.get("citations", [])
    
    if citations:
        for i, cit in enumerate(citations, 1):
            score = cit.get('score', 0)
            score_color = "#28a745" if score >= 0.8 else "#fd7e14" if score >= 0.6 else "#dc3545"
            
            st.markdown(f"""
            <div class="citation-box">
                <strong>📄 Source {i}</strong><br>
                <strong>Document:</strong> {cit.get('path', 'Unknown')}<br>
                <strong>Section:</strong> {cit.get('section', 'Unknown')}<br>
                <strong>Relevance Score:</strong> <span style="color: {score_color}; font-weight: bold;">{score:.1%}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Retrieved Passages Section - FIXED TO SHOW ACTUAL TEXT
    if show_raw and citations:
        st.markdown("---")
        st.markdown("### 📄 Full Retrieved Passage Content")
        st.info("💡 These are the actual text excerpts from the guidelines that were retrieved and used to generate the answer.")
        
        for i, cit in enumerate(citations, 1):
            passage_text = cit.get('text', 'No text available')
            
            with st.expander(f"📖 Passage {i}: {cit['path']} - {cit['section']}", expanded=(i==1)):
                st.markdown(f"""
                <div class="passage-box">
                    <div class="passage-header">
                        Source {i} | Document: {cit['path']} | Section: {cit['section']} | Relevance: {cit['score']:.1%}
                    </div>
                    <div class="passage-text">{passage_text}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Raw JSON (for developers)
    with st.expander("🔍 View Raw API Response (Developer Mode)"):
        st.json(result)

# History section
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Recent Query History")
    
    for i, item in enumerate(st.session_state.history[:5]):
        conf = item['result'].get('confidence', 0)
        status = item['result'].get('status', 'unknown')
        
        with st.expander(f"🕐 {item['timestamp']} | {status.upper()} | Conf: {conf:.1%}", expanded=False):
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Answer:** {item['result'].get('answer', '')[:300]}...")
            
            if st.button(f"🔄 Ask Again", key=f"reload_{i}"):
                st.session_state.question_text = item['question']
                st.session_state.trigger_query = True
                st.rerun()

# Footer
st.markdown("---")
st.caption("🏥 Healthcare Guidelines RAG Assistant | Powered by FastAPI + Groq LLM + FAISS + Sentence Transformers | v0.4.0")
st.caption("Built with ❤️ for Evidence-Based Healthcare Practice")