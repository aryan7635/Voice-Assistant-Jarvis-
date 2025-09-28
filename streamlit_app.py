import streamlit as st
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.types import ConversationConfig
import os
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")
USER_ID = os.getenv("USER_ID", "Aryan")

# Error handling for missing config
if not AGENT_ID or not API_KEY:
    st.error("Missing AGENT_ID or API_KEY. Please set them in your environment variables or .env file.")
    st.stop()

st.title("Voice Assistant (ElevenLabs)")

prompt = st.text_area("Assistant Prompt", "You are a helpful assistant. How can I help you today?")
first_message = st.text_input("First Message", f"Hello {USER_ID}, how can I help you today?")

conversation_override = {
    "agent": {
        "prompt": {"prompt": prompt},
        "first_message": first_message,
    },
}

config = ConversationConfig(
    user_id=USER_ID,
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

client = ElevenLabs(api_key=API_KEY)
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Your Message")
if st.button("Send") and user_input:
    response = conversation.send_message(user_input)
    st.session_state["messages"].append(("User", user_input))
    st.session_state["messages"].append(("Assistant", response))

for sender, msg in st.session_state["messages"]:
    st.write(f"**{sender}:** {msg}")
