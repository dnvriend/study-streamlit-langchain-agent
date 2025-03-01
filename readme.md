# study-streamlit-langchain-agent
This project implements VIC, an intelligent conversational agent built with LangChain and powered by Claude 3.7 Sonnet on AWS Bedrock. VIC is designed to assist users in understanding complex topics and accelerating scientific discovery through thoughtful, inquisitive interactions.

## Project Overview

VIC (inspired by the VIC-20 computer) is a versatile, high-performance AI assistant that can:
- Engage in natural conversations with users
- Access and use various tools to perform tasks
- Demonstrate "thinking" capabilities to show its reasoning process
- Maintain conversation history for contextual responses

## Key Components

- **LangChain Integration**: Uses LangChain's agent framework to orchestrate tool usage and conversation flow
- **AWS Bedrock**: Leverages Claude 3.7 Sonnet and other Claude models via AWS Bedrock
- **Streamlit UI**: Provides a clean, interactive web interface for chatting with VIC
- **Tool Integration**: Includes tools for:
  - Shell command execution
  - Python REPL for code execution
  - HTTP requests
  - Time retrieval

## Implementation Details

VIC is implemented as a LangChain agent with:
- Custom system prompt that defines VIC's personality and capabilities
- Tool-calling capabilities to execute external functions
- Conversation memory to maintain context
- Streaming responses for real-time interaction
- "Thinking" mode that exposes the agent's reasoning process

The Streamlit interface provides model selection options and displays both the conversation and VIC's thinking process in real-time.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS credentials for Bedrock access
3. Run the application: `streamlit run main.py`
