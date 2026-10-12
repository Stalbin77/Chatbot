import streamlit as st
from service import ChatService

# Page configuration
st.set_page_config(
    page_title="MACET Chatbot",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Welcome to MACET Chatbot! 🤖")
st.caption("Powered by Ollama and Llama 3.2")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize ChatService once per Streamlit session
if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService(model="llama3.2")

chat_service = st.session_state.chat_service

# Optional: clear conversation
with st.sidebar:
    st.header("Chat Settings")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything!")

if prompt:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and stream assistant response
    with st.chat_message("assistant"):
        try:
            response = st.write_stream(
                chat_service.generate_stream(
                    st.session_state.messages
                )
            )

            # Save the completed assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": str(response) if response is not None else "",
            })

        except Exception as e:
            st.error(
                "Unable to generate a response. "
                "Please check that Ollama is running and the model is available."
            )
            st.exception(e)