import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Apply custom styles for the app
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    .stSelectbox svg {
        fill: white !important;
    }
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Set up the app title and caption
st.title("🧠 Chat with Emtu AI")
st.caption("🔥 Ask anything, get instant responses!")

# Sidebar configuration for selecting model and other settings
with st.sidebar:
    st.header("🚀 Welcome to Emtu ChatBot")
    st.divider()

    st.header("⚙️ Config")
    selected_model = st.selectbox("Choose Model", ['deepseek-r1:1.5b'], index=0)
    st.divider()

    st.markdown("""
    **🌟 What’s Next?**  
    - 🤖 Smarter AI responses  
    - ⚡ Faster performance  
    - 🔍 Improved accuracy  
    - 🌐 Multilingual support  
    - 🎯 Personalized AI experience
    """)
    st.divider()

    st.markdown("Built with [Ollama](https://ollama.com/) | [LangChain](https://www.langchain.com/)")
    st.divider()
    st.markdown("Created by Tanjil Mahmud Emtu")

# Initialize the chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",  # Fixed missing quote
    temperature=0.3
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are Emtu AI, a highly intelligent assistant built by Emtu. "
    "You were created by Tanjil Mahmud Emtu, a passionate AI and programming enthusiast. "
    "Your task is to provide insightful, helpful, and friendly responses to all user queries. "
    "You should assist users with programming questions, AI topics, and general knowledge. "
    "Always be concise, clear, and respectful in your replies. "
    "Feel free to explain concepts in simple terms if the user is a beginner. "
    "Your goal is to make sure the user gets the information they need in the best way possible. "
    "If a user asks who created you?, simply say: 'I was created by Tanjil Mahmud Emtu, a passionate AI and programming enthusiast."
)

# Session state management to store message log
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I am Emtu AI. How can I help you?"}]

# Display chat container
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Process user input and generate AI response
user_query = st.chat_input("Type your question here...")

def generate_ai_response(prompt_chain):
    try:
        processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
        return processing_pipeline.invoke({})
    except httpx.ConnectError:
        return "⚠️ Connection error: Unable to reach the AI model. Please check if Ollama is running."

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

# Handle user input and AI response
if user_query:
    # Add user query to message log
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)

    # Add AI response to message log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    # Rerun to update chat display
    st.rerun()
