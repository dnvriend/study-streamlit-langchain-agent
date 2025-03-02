from claude_bedrock import get_agent_executor_chat_bedrock_converse, MODEL_SONNET_37
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
from streaming_response_callback_handler import StreamingResponseCallbackHandler

# Initialize memory
if "memory" not in st.session_state:
    msgs = StreamlitChatMessageHistory(key="chat_messages")
    if not msgs.messages:
        msgs.add_ai_message("How can I help you?")
    st.session_state.memory = ConversationBufferWindowMemory(
        chat_memory=msgs, return_messages=True, memory_key="chat_history", k=500
    )

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Sonnet 3.7:1.0"
if "username" not in st.session_state:
    st.session_state.username = "Guest"

# Initialize agent executor
agent_executor = get_agent_executor_chat_bedrock_converse(
    option=st.session_state.selected_model,
    memory=st.session_state.memory,
    max_iterations=25,
    streaming=True,
    thinking=True,
    username=st.session_state.username,
)

# Page config
st.set_page_config(page_title="Bot", page_icon=":bot:", layout="wide")

# Sidebar
st.sidebar.title("Settings")
username_input = st.sidebar.text_input("Enter your name", value="Dennis")
if st.sidebar.button("Set Username"):
    st.session_state.username = username_input
    agent_executor = get_agent_executor_chat_bedrock_converse(
        option=st.session_state.selected_model,
        memory=st.session_state.memory,
        max_iterations=25,
        streaming=True,
        thinking=True,
        username=st.session_state.username,
    )

model_options = ["Sonnet 3.7:1.0", "Sonnet 3.5:2.0", "Sonnet 3.5:1.0"]
selected_model = st.sidebar.selectbox("Select a model", model_options)
if st.sidebar.button("Apply Model"):
    st.session_state.selected_model = selected_model
    agent_executor = get_agent_executor_chat_bedrock_converse(
        option=st.session_state.selected_model,
        memory=st.session_state.memory,
        max_iterations=25,
        streaming=True,
        thinking=True,
        username=st.session_state.username,
    )

st.sidebar.metric("History Size", len(st.session_state.memory.chat_memory.messages))

# Main UI
st.title("VIC-20 Human Assistant")
chat_container = st.container()

# Display initial chat history
with chat_container:
    for msg in st.session_state.memory.chat_memory.messages:
        if msg.type == "ai" and isinstance(msg.content, list):
            pass
        else:
            with st.chat_message(msg.type):
                st.markdown(msg.content)

# User input
user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    with chat_container:
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st_callback = StreamlitCallbackHandler(parent_container=st.container(), expand_new_thoughts=True, max_thought_containers=10, collapse_completed_thoughts=True)
                stream_handler = StreamingResponseCallbackHandler(thinking_area=st.empty(), text_area=st.empty())
                agent_executor.invoke({"input": user_query}, config={"callbacks": [stream_handler, st_callback]})
    st.session_state.memory.save_context({"input": user_query}, {"output": stream_handler.text})