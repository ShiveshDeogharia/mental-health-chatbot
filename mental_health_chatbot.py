import streamlit as st
import ollama
import base64
import os

st.set_page_config(page_title="Mental Health Chatbot", layout="centered")

def get_base64(background):
    with open(background, "rb") as f:
        return base64.b64encode(f.read()).decode()


bg_path = "background.png"
if os.path.exists(bg_path):
    bin_str = get_base64(bg_path)
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

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

def generate_response(user_input):
    """Generate chatbot response and update history."""
    st.session_state["conversation_history"].append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="llama3.1:8b", messages=st.session_state["conversation_history"])
        ai_response = response.get("message", {}).get("content", "I'm here to help!")
    except Exception as e:
        ai_response = "Sorry, I couldn't process that request."

    st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    """Fetch a positive affirmation."""
    prompt = "Provide a positive affirmation for someone feeling stressed."
    try:
        response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "You're doing great! Keep going.")
    except Exception as e:
        return "Stay positive and believe in yourself!"

def generate_meditation_guide():
    """Fetch a short guided meditation script."""
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    try:
        response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Take a deep breath and relax...")
    except Exception as e:
        return "Focus on your breath, let go of worries, and be present."

st.title("🧘 Mental Health Support Agent")


for msg in st.session_state["conversation_history"]:
    role = "You" if msg["role"] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

user_message = st.text_input("How can I help you today?")

if user_message.strip():
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")


col1, col2 = st.columns(2)

with col1:
    if st.button("💬 Positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("🧘 Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
