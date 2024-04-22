import os
import time
import base64
import re
import json
import streamlit as st
import openai

# Load environment variables from a file
def load_env_variables(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip()

# Initialize the OpenAI client
def initialize_client():
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if azure_openai_endpoint and azure_openai_key:
        client = openai.AzureOpenAI(api_key=azure_openai_key, api_version="2024-02-15-preview", azure_endpoint=azure_openai_endpoint)
    else:
        client = openai.OpenAI(api_key=openai_api_key)
    return client

client = initialize_client()
assistant_id = os.environ.get("ASSISTANT_ID")

# Create a thread with initial user message and enable file search
def create_thread(user_input):
    thread = client.Thread.create(
        assistant_id=assistant_id, 
        messages=[{"role": "user", "content": user_input}],
        file_search={"enabled": True}
    )
    return thread

# Post user messages to the thread
def post_message(thread_id, user_input):
    message = client.Message.create(
        thread_id=thread_id,
        role='user',
        content={"text": user_input}
    )
    return message

# Fetch messages from a thread
def fetch_messages(thread_id):
    messages = client.Message.list(thread_id=thread_id)
    return messages

# Main application logic for Streamlit UI
def main():
    st.title("Assistant V2 Interface")
    user_input = st.text_input("Enter your query:")
    if user_input:
        thread = create_thread(user_input)
        time.sleep(1)  # Sleep to allow time for assistant to respond
        messages = fetch_messages(thread.id)
        for message in messages.data:
            if message.role == 'assistant':
                st.write(message.content.text)

if __name__ == "__main__":
    # load_env_variables('.env')
    main()
