import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "e103b380-ebad-43dc-b58b-0cafc3c2895e"
FLOW_ID = "7952e24a-85fa-4543-8222-50dbffe75aba"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "social_media"

# Helper function to extract message
def extract_message(response_data):
    try:
        outputs = response_data["outputs"][0]["outputs"][0]["results"]["message"]
        return outputs.get("text", "")
    except (KeyError, IndexError):
        return None

# Function to run flow
def run_flow(message: str) -> str:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        message_content = extract_message(response.json())
        return message_content if message_content else "Could not process response"
    except requests.exceptions.RequestException as e:
        return f"Error making request: {str(e)}"

# Function to style chat messages
def styled_chat_message(role, content):
    icon = "👤" if role == "user" else "🤖"
    style = {
        "user": {"background-color": "#102c35", "border-radius": "15px", "padding": "10px"},  # Light Blue
        "assistant": {"background-color": "#4d5b60", "border-radius": "15px", "padding": "10px"}  # Lavender
    }
    message_style = style[role]
    st.markdown(
        f"<div style='background-color: {message_style['background-color']}; "
        f"border-radius: {message_style['border-radius']}; padding: {message_style['padding']}; "
        f"margin-bottom: 10px;'>"
        f"{icon} {content}</div>",
        unsafe_allow_html=True
    )

# Main app
def main():
    # Title and description
    st.title("Social Media Insights Analyzer")
    st.write("Gain insights into your social media engagement with the power of LangFlow and Astra DB.")

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Display chat messages
    for message in st.session_state.messages:
        styled_chat_message(message["role"], message["content"])
    
    # Input box for user prompt
    if prompt := st.chat_input("Ask about your social media insights..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        styled_chat_message("user", prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                result = run_flow(prompt)
                if result:
                    styled_chat_message("assistant", result)
                    st.session_state.messages.append({"role": "assistant", "content": result})

    # Sidebar content
    st.sidebar.title("About")
    st.sidebar.info("This chatbot analyzes social media engagement data using LangFlow and Astra DB.")
    with st.sidebar.expander("More Info"):
        st.info("Set your application token in the `.env` file for secure API access.")
        st.info("Ask questions to uncover trends, engagement insights, and audience sentiment.")

    st.sidebar.markdown("---")
    st.sidebar.write("Built with ❤️ using [Streamlit](https://streamlit.io) and [LangFlow](https://langflow.io)")

if __name__ == "__main__":
    main()
