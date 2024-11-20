import streamlit as st
from openai import OpenAI
import requests  # Library for making HTTP requests (for internet access)

# Embed the API key directly (NOT recommended for production)
OPENAI_API_KEY = "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"

# Show title and description
st.title("💬 Chatbot with Internet Access")
st.write(
    "This chatbot uses OpenAI's models to generate responses and access the internet. "
    "The app demonstrates how to interact with models and fetch information online."
)

# API key handling
openai_api_key = OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

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

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Ask me anything (e.g., 'Search for latest news'):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if the user wants to fetch something online
    if "search" in prompt.lower():
        with st.chat_message("assistant"):
            try:
                # Perform a search using a public API or web scraper
                search_query = prompt.lower().replace("search", "").strip()
                response = requests.get(
                    f"https://api.duckduckgo.com/?q={search_query}&format=json"
                )
                search_result = response.json().get("AbstractText", "No results found.")
                st.markdown(f"Search Result: {search_result}")
                st.session_state.messages.append({"role": "assistant", "content": search_result})
            except Exception as e:
                error_message = f"Failed to fetch search results: {e}"
                st.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        # Generate a response using the selected OpenAI model
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Stream the response to the chat
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_message = f"An error occurred: {e}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
