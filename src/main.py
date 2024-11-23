import os
import json
import requests
import streamlit as st

# Load Hugging Face API Key from config
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
HUGGINGFACE_API_KEY = config_data[
    "OPENAI_API_KEY"]  # Assuming the Hugging Face API key is stored under "OPENAI_API_KEY"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Configuring Streamlit page settings
st.set_page_config(
    page_title="GPT-4o Chat",
    page_icon="🗯",
    layout="centered"
)

# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask GPT...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Send the user's message to Hugging Face's text generation model
    api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"  # You can replace "gpt2" with another model from Hugging Face
    payload = {"inputs": user_prompt}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        assistant_response = response.json()[0]['generated_text']  # Extracting the generated text
    except requests.exceptions.RequestException as e:
        assistant_response = f"Error: {e}"

    # Append the assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
