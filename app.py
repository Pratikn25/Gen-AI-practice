import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# App title and instructions
st.title("💬 Champak's Chatbot")
st.write("Your personal relationship therapist ✨")

# Ask for user name only once
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input("Hi there! What's your name?")
    if not st.session_state.user_name:
        st.stop()  # Stop until user enters name

# Define initial role/prompt
Initial_prompt = (
    f"You are Champak, a kind, empathetic, and emotionally supportive relationship therapist. "
    f"You are talking to a user named {st.session_state.user_name}. "
    f"You provide thoughtful, non-judgmental advice like a wise, playful friend. "
    f"Make your output concise and crisp as much as possible."
    f"Stay like this for the whole conversation."
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [Initial_prompt]}]

# Chat input box
user_input = st.chat_input(f"Hi {st.session_state.user_name}, what's on your mind?")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    # Generate model response
    response = model.generate_content(st.session_state.chat_history)

    # Add model response to history
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

# Show chat history (excluding the initial prompt)
for i, msg in enumerate(st.session_state.chat_history):
    if i == 0:
        continue  # skip initial instruction
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **{st.session_state.user_name}:** {msg['parts'][0]}")
    elif msg["role"] == "model":
        st.markdown(f"🧠 **Champak:** {msg['parts'][0]}")
