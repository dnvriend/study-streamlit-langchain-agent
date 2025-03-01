import streamlit as st
from claude_bedrock import get_agent_executor_chat_bedrock_converse
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.callbacks.streamlit.streamlit_callback_handler import (
    StreamlitCallbackHandler,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        return_messages=True, memory_key="chat_history", k=500
    )

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Sonnet 3.7:1.0"

# Initialize agent executor
agent_executor = get_agent_executor_chat_bedrock_converse(
    st.session_state.selected_model, st.session_state.memory
)

# page config
st.set_page_config(page_title="Bot", page_icon=":bot:", layout="wide")

# Sidebar
st.sidebar.title("Settings")
model_options = ["Sonnet 3.7:1.0", "Sonnet 3.5:2.0", "Sonnet 3.5:1.0"]
selected_model = st.sidebar.selectbox("Select a model", model_options)
# Model selection

if st.sidebar.button("Apply Model"):
    st.session_state.selected_model = selected_model
    st.rerun()

# Display history size
history_size = len(st.session_state.messages)
st.sidebar.metric("History Size", history_size)

st.title("Chatbot")

user_query = st.chat_input("Your message")

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)


if user_query is not None and user_query != "":
    st.session_state.messages.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st_callback = StreamlitCallbackHandler(
                st.container(),
                expand_new_thoughts=True,
                max_thought_containers=10,
                collapse_completed_thoughts=True,
            )
            config = {"callbacks": [st_callback]}
            response = agent_executor.invoke({"input": user_query}, config=config)
            
            # Handle different output formats
            output = response["output"]
            if isinstance(output, str):
                ai_message = output
                print("normal output, plain string")
            else:
                try:
                    # Handle the new output format with reasoning_content and text types
                    thinking_content = []
                    response_content = []
                    
                    for item in output:
                        if isinstance(item, dict):
                            if item.get("type") == "reasoning_content" and "reasoning_content" in item:
                                # Extract thinking content
                                reasoning = item["reasoning_content"].get("text", "")
                                if reasoning:
                                    thinking_content.append(reasoning)
                                    # Display thinking in a special box
                                    with st.expander("Claude's Thinking Process", expanded=True):
                                        st.markdown(reasoning)
                            
                            elif item.get("type") == "text" and "text" in item:
                                # Extract response text
                                response_content.append(item["text"])
                            
                            # Handle legacy format with just text key
                            elif "text" in item:
                                response_content.append(item["text"])
                    
                    # Combine all response content
                    if response_content:
                        ai_message = "\n".join(response_content)
                    else:
                        # Fallback if no response content found
                        ai_message = str(output)
                        st.warning("Unexpected response format received from the agent")
                    
                    print(f"Processed output with {len(thinking_content)} thinking items and {len(response_content)} response items")
                
                except (TypeError, KeyError) as e:
                    st.warning(f"Unexpected response format: {str(e)}")
                    ai_message = str(output)
                    print(f"unexpected output format: {str(e)}")
            
            st.markdown(ai_message)

    st.session_state.messages.append(AIMessage(ai_message))
    st.session_state.memory.chat_memory.add_user_message(user_query)
    st.session_state.memory.chat_memory.add_ai_message(ai_message)
