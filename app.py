import asyncio
import uuid

import streamlit as st
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agent import create_travel_agent

st.set_page_config(page_title="Family Travel Planner", page_icon="✈️")

st.title("Family Travel Planner AI")
st.markdown("Welcome! I can help plan our next trip. Just tell me where you want to go!")

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

def _get_or_create_event_loop():
    loop = st.session_state.get("event_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state.event_loop = loop
    return loop


def _run_coroutine(coroutine):
    loop = _get_or_create_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


async def _initialize_agent_state():
    agent = create_travel_agent()
    session_service = InMemorySessionService()
    app_name = "travel_app"
    user_id = "family"
    session_id = st.session_state.get("session_id")
    if not session_id:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        st.session_state.session_id = session_id

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    return agent, runner, session_service, session, app_name, user_id


async def _run_agent(prompt: str) -> str:
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in st.session_state.runner.run_async(
        user_id=st.session_state.user_id,
        session_id=st.session_state.session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text:
                return text
    return "I couldn't generate a response. Please try again."


def ensure_agent_initialized():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.get("agent_initialized"):
        return

    try:
        (
            st.session_state.agent,
            st.session_state.runner,
            st.session_state.session_service,
            st.session_state.session,
            st.session_state.app_name,
            st.session_state.user_id,
        ) = _run_coroutine(_initialize_agent_state())
        st.session_state.agent_initialized = True
    except Exception as e:
        st.session_state.agent_initialized = False
        st.error(f"Failed to initialize agent: {e}")


ensure_agent_initialized()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Where should we go next?"):
    ensure_agent_initialized()
    if not st.session_state.get("runner"):
        st.error("Agent is not ready yet. Please try again.")
        st.stop()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            full_response = _run_coroutine(_run_agent(prompt))
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            message_placeholder.markdown(f"Error: {e}")

