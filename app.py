import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from memory_handler import MemoryHandler
from llm_connector import LLMConnector

CUSTOM_CSS = """
<style>
    /* Main App Background & Typography */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Restrict Main Content Width & Center It */
    .main .block-container {
        max-width: 800px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 auto !important;
    }

    /* Header Container */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 20px 0 16px 0;
        border-bottom: 1px solid #2E3856;
        margin-bottom: 24px !important;
        text-align: center;
    }
    .header-title-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .header-badge {
        background: rgba(30, 41, 59, 0.6);
        color: #38BDF8;
        border: 1px solid rgba(14, 165, 233, 0.4);
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
    }

    /* Welcome Card */
    .hero-card {
        background: linear-gradient(135deg, #1E2640 0%, #151B2C 100%);
        border: 1px solid #2E3856;
        border-radius: 16px;
        padding: 24px 24px;
        text-align: center;
        margin: 0 auto 30px auto !important;
        max-width: 600px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .hero-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Center Chat Input Bar */
    .stChatInputContainer {
        max-width: 800px !important;
        margin: 0 auto !important;
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
    }
</style>
"""

class StreamlitChatUI:
    def __init__(self):
        st.set_page_config(
            page_title="Memora AI",
            page_icon="⚡",
            layout="centered",
            initial_sidebar_state="expanded"
        )
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "memory_handler" not in st.session_state:
            st.session_state.memory_handler = MemoryHandler(user_id="user_demo")

        if "llm_connector" not in st.session_state:
            st.session_state.llm_connector = LLMConnector(model_name="llama-3.3-70b-versatile")

    def render_header(self):
        st.markdown(
            """
            <div class="header-container">
                <div class="header-title-row">
                    <h1 class="header-title">⚡ Memora AI</h1>
                </div>
                <span class="header-badge">Groq LLaMA 3.3 + Mem0 Engine</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("### 🧠 Memory Vault")
            st.caption("Facts extracted automatically and synced to Mem0 Cloud.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Sync", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("🗑️ Wipe All", use_container_width=True, type="primary"):
                    try:
                        st.session_state.memory_handler.wipe_all_memories()
                        st.session_state.messages = []
                        st.toast("Wiped memory vault!", icon="🧹")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error wiping memories: {e}")

            st.divider()

            try:
                memories_data = st.session_state.memory_handler.get_all_memories_detailed()
                st.metric(label="Saved Facts", value=len(memories_data))
                st.write("")

                if memories_data:
                    for i, mem_obj in enumerate(memories_data, 1):
                        mem_id = mem_obj.get("id")
                        mem_text = mem_obj.get("memory", "")
                        
                        card_col, del_col = st.columns([0.85, 0.15])
                        with card_col:
                            st.info(f"**#{i}:** {mem_text}")
                        with del_col:
                            if st.button("❌", key=f"del_{mem_id}"):
                                st.session_state.memory_handler.delete_single_memory(mem_id)
                                st.toast(f"Deleted Fact #{i}", icon="🗑️")
                                st.rerun()
                else:
                    st.info("Vault is empty! Tell me facts about yourself.")
            except Exception as e:
                st.error(f"Vault sync error: {e}")

    def render_chat(self):
        # Render welcome box directly under header line if chat is empty
        if not st.session_state.messages:
            st.markdown(
                """
                <div class="hero-card">
                    <div class="hero-title">Welcome to Memora AI</div>
                    <div class="hero-subtitle">
                        I remember facts about you across every session.<br>
                        Tell me about your age, location, hobbies, or preferences to get started!
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Render conversation history
        for message in st.session_state.messages:
            avatar = "👤" if message["role"] == "user" else "⚡"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
                if "retrieved_mems" in message and message["retrieved_mems"]:
                    with st.expander("🔍 Retreived Context from Mem0"):
                        st.text(message["retrieved_mems"])

        # Chat Input
        if user_input := st.chat_input("Ask a question or share details about yourself..."):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.rerun()

    def process_latest_input(self):
        # Generate LLM response if the last turn was user input
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            user_input = st.session_state.messages[-1]["content"]

            relevant_mems = st.session_state.memory_handler.get_memories(user_input)

            with st.chat_message("assistant", avatar="⚡"):
                with st.spinner("Retrieving memory & generating..."):
                    bot_response = st.session_state.llm_connector.generate_response(
                        user_message=user_input,
                        relevant_memories=relevant_mems or "No relevant memories.",
                        chat_history=st.session_state.messages[:-1]
                    )
                    st.markdown(bot_response)
                    
                    if relevant_mems:
                        with st.expander("🔍 Retreived Context from Mem0"):
                            st.text(relevant_mems)

            assistant_msg = {
                "role": "assistant", 
                "content": bot_response, 
                "retrieved_mems": relevant_mems
            }
            st.session_state.messages.append(assistant_msg)
            
            # FIXED: Passing only 1 argument to match MemoryHandler definition
            st.session_state.memory_handler.add_memory(user_input)
            st.rerun()


if __name__ == "__main__":
    ui = StreamlitChatUI()
    ui.render_header()
    ui.render_sidebar()
    ui.render_chat()
    ui.process_latest_input()
