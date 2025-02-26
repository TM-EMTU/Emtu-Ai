import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Apply custom styles for a dark UI
st.markdown("""
<style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #2d2d2d; }
    .stTextInput textarea, .stSelectbox div[data-baseweb="select"],
    .stSelectbox option, div[role="listbox"] div {
        color: white !important; background-color: #3d3d3d !important;
    }
    .stSelectbox svg { fill: white !important; }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🧠 Chat with Emtu AI")
st.caption("🔥 Ask anything, get instant responses!")

# Sidebar Config
with st.sidebar:
    st.header("🚀 Welcome to Emtu ChatBot")
    st.divider()
    st.header("⚙️ Config")
    selected_model = st.selectbox("Choose Model", ["gemini-2.0-pro", "gemini-2.0-flash"], index=1)
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
    st.markdown("Built with [Gemini AI](https://ai.google.dev/)")
    st.divider()
    st.markdown("Created by **Tanjil Mahmud Emtu**")

# Initialize API Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# System Prompt
system_prompt = (
    "You are Emtu AI, a highly intelligent assistant built by Tanjil Mahmud Emtu. "
    "Your task is to provide insightful, helpful, and friendly responses to user queries, "
    "especially in programming, AI, and general knowledge. Always be clear and respectful. "
    "If a user asks who created you, respond with: 'I was created by Tanjil Mahmud Emtu, a passionate AI and programming enthusiast.'"
)

# Session State for Chat Log
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {"role": "ai", "content": "Hi! I am Emtu AI. How can I help you?"}
    ]

# Display Chat History
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to Generate AI Response
def generate_ai_response(user_message):
    try:
        # Request to Gemini AI
        response = client.models.generate_content(
            model=selected_model,
            contents=[user_message],
        )
        return response.text if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# User Input
user_query = st.chat_input("Type your question here...")

# Process User Query
if user_query:
    # Add User Message
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Generate AI Response
    with st.spinner("🧠 Processing..."):
        ai_response = generate_ai_response(user_query)

    # Add AI Response to Message Log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    # Refresh UI
    st.rerun()
