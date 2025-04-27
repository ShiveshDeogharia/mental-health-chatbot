import streamlit as st
import ollama
import base64
import os


st.set_page_config(page_title="Mental Health Chatbot", layout="centered")


def get_base64(background_path):
    with open(background_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(background_path):
    if os.path.exists(background_path):
        bin_str = get_base64(background_path)
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{bin_str}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                }}
            </style>
        """, unsafe_allow_html=True)

def generate_response(user_input):
    """Send user input to Ollama and get AI response."""
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(model="llama3:8b", messages=st.session_state.conversation_history)
        ai_response = response.get("message", {}).get("content", "I'm here to support you!")
    except Exception as e:
        ai_response = "Sorry, I'm currently unable to respond. Please try again later."
        st.error("⚠️ Unable to connect to the AI backend. Make sure Ollama is running.")
    st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    """Fetch a positive affirmation."""
    prompt = "Give a positive affirmation for someone feeling stressed."
    try:
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "You are stronger than you think!")
    except Exception:
        return "Stay positive and believe in yourself!"

def generate_meditation_guide():
    """Fetch a short guided meditation script."""
    prompt = "Provide a 5-minute guided meditation script for stress relief."
    try:
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Take a deep breath and relax...")
    except Exception:
        return "Close your eyes, breathe deeply, and let go of all worries."


set_background("background.png")  


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


st.title("🧘 Mental Health Support Agent")


for msg in st.session_state.conversation_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])


user_input = st.chat_input("How can I support you today?")

if user_input:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_input)
        with st.chat_message("assistant"):
            st.markdown(ai_response)


st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Positive Affirmation"):
        affirmation = generate_affirmation()
        st.success(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("🧘 Guided Meditation"):
        meditation = generate_meditation_guide()
        st.info(f"**Meditation Guide:** {meditation}")

with col3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.conversation_history = []
        st.experimental_rerun()

