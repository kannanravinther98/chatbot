import streamlit as st
import openai
import requests

# Embed the API key directly (NOT recommended for production)
OPENAI_API_KEY = "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"

# Show title and description
st.title("💬 Smart Chatbot with Automatic Internet Access")
st.write(
    "This chatbot uses OpenAI's models to generate responses and fetch "
    "real-time information online when required."
)

# API key handling
openai.api_key = OPENAI_API_KEY

# Sidebar settings
st.sidebar.title("Settings")
model = st.sidebar.selectbox(
    "Select a model",
    options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
    index=0,
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to fetch online data
def fetch_online_data(query):
    try:
        response = requests.get(
            f"https://api.duckduckgo.com/?q={query}&format=json"
        )
        if response.status_code == 200:
            return response.json().get("AbstractText", "No results found.")
        return "Failed to fetch results."
    except Exception as e:
        return f"Error fetching data: {e}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Ask me anything (e.g., 'Search for latest news'):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Flag to decide if online data is needed
    fetch_online = any(keyword in prompt.lower() for keyword in ["search", "news", "info", "lookup"])
    online_data = None

    try:
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        # Get the initial OpenAI response
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )

        # Extract the response content
        response_content = response.choices[0].message["content"]

        # Check if OpenAI indicates a lack of knowledge or fetch_online flag is set
        if "do not have real-time capabilities" in response_content or fetch_online:
            st.info("Fetching online information for the latest updates...")
            online_data = fetch_online_data(prompt)
            response_content += f"\n\nOnline Information: {online_data}"

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response_content)
        st.session_state.messages.append({"role": "assistant", "content": response_content})
    except Exception as e:
        error_message = f"An error occurred: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
