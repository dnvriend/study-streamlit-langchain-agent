# Langchain agent with streaming output

This example demonstrates how to create a Streamlit application with a LangChain agent that provides streaming output, including both the final response and the agent's "thinking" process.

## Key Components

### StreamlitChatMessageHistory

The application uses `StreamlitChatMessageHistory` to store conversation history in Streamlit's session state:

- It persists messages across app reruns within a user session
- Messages are stored at a specified key in session state (default: "langchain_messages")
- It provides methods like `add_user_message()` and `add_ai_message()` to manage the conversation

### ConversationBufferWindowMemory

`ConversationBufferWindowMemory` is used to maintain conversation context:

- It's initialized with `StreamlitChatMessageHistory` as its `chat_memory`
- The `k=500` parameter limits memory to the 500 most recent exchanges
- `return_messages=True` ensures memory is returned as message objects
- `memory_key="chat_history"` defines how memory is accessed in the prompt

### Custom StreamHandler

The `StreamHandler` class enables real-time streaming of the model's output:

- It inherits from `BaseCallbackHandler` and implements `on_llm_new_token`
- It manages two separate output areas: one for the final response and one for "thinking"
- It parses different token types from the model (text, tool results, reasoning)
- It updates the UI in real-time as tokens arrive

### StreamlitCallbackHandler

The `StreamlitCallbackHandler` is crucial for visualizing the agent's tool usage:

- It displays tool calls, inputs, and outputs in the Streamlit UI
- It must be included in the callbacks list for tool visualization to work
- It provides options to expand/collapse thoughts and control their display

## Implementation Flow

1. Initialize conversation memory with StreamlitChatMessageHistory
2. Set up the agent executor with streaming enabled
3. Display existing chat history from memory
4. Process user input and stream the response using both handlers
5. Save the conversation context back to memory


## Code

```python
from claude_bedrock import get_agent, MODEL_SONNET_37
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.callbacks import BaseCallbackHandler
import streamlit as st
from claude_bedrock import get_agent_executor_chat_bedrock_converse
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, thinking_area, text_area):
        self.thinking_area = thinking_area
        self.thinking_text = ""
        self.text_area = text_area
        self.text = ""

    def on_llm_new_token(self, token: list[dict], **kwargs):
        """Handle new tokens from the LLM."""
        text_result = ""
        thinking_result = ""
        try:
            for item in token:
                if item.get('type') and item['type'] == 'text':
                    text_result += item['text']
                elif item.get('type') and item['type'] == 'tool_result':
                    text_result += item['text']
                elif item.get('type') and item['type'] == 'reasoning_content' and item['reasoning_content']['type'] == 'text':
                    # Use HTML italic tags instead of Markdown asterisks
                    thinking_result += f"<i style='color: darkgray;'>{item['reasoning_content']['text']}</i>"
        except Exception as e:
            print(f"Error: {e}")
            print(f"Token: {token}")
        self.text += text_result
        self.thinking_text += thinking_result
        self.text_area.markdown(self.text)
        self.thinking_area.markdown(self.thinking_text, unsafe_allow_html=True)

# Initialize memory with StreamlitChatMessageHistory
if "memory" not in st.session_state:
    # Create the history object
    msgs = StreamlitChatMessageHistory(key="chat_messages")
    # Add a welcome message if history is empty
    if not msgs.messages:
        msgs.add_ai_message("How can I help you?")
    # Set up memory with StreamlitChatMessageHistory as chat_memory
    st.session_state.memory = ConversationBufferWindowMemory(
        chat_memory=msgs,
        return_messages=True,
        memory_key="chat_history",
        k=500
    )

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Sonnet 3.7:1.0"

# Initialize agent executor
agent_executor = get_agent_executor_chat_bedrock_converse(
    option=st.session_state.selected_model,
    memory=st.session_state.memory,
    max_iterations=25,
    streaming=True,
    thinking=True,
)

# Page config
st.set_page_config(page_title="Bot", page_icon=":bot:", layout="wide")

# Sidebar
st.sidebar.title("Settings")
model_options = ["Sonnet 3.7:1.0", "Sonnet 3.5:2.0", "Sonnet 3.5:1.0"]
selected_model = st.sidebar.selectbox("Select a model", model_options)

if st.sidebar.button("Apply Model"):
    st.session_state.selected_model = selected_model
    st.rerun()

# Display history size
msgs = st.session_state.memory.chat_memory
history_size = len(msgs.messages)
st.sidebar.metric("History Size", history_size)

# Main UI
st.title("Chatbot")

# Display chat history
for msg in msgs.messages:
    if msg.type == "ai" and isinstance(msg.content, list):
        pass
    else:
        with st.chat_message(msg.type):
            st.markdown(msg.content)

# User input
user_query = st.chat_input("Your message")

if user_query is not None and user_query != "":
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_query)

    # Process and stream assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st_callback = StreamlitCallbackHandler( st.container(), expand_new_thoughts=True, max_thought_containers=10, collapse_completed_thoughts=True)
            stream_handler = StreamHandler(st.empty(), st.empty())
            response = agent_executor.invoke({"input": user_query}, {"callbacks": [stream_handler, st_callback]})            

    # Save the conversation to memory
    st.session_state.memory.save_context({"input": user_query}, {"output": stream_handler.text})
```