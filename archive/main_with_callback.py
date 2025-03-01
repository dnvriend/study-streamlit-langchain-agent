from claude_bedrock import get_agent, MODEL_SONNET_37
from langchain.memory import ConversationBufferMemory
from langchain_core.callbacks import BaseCallbackHandler

class ConsoleCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to the console in a structured format."""

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        """Handle the start of an LLM thought."""
        print("• Thinking...")
        print("  LLM: ", end="")

    def on_llm_new_token(self, token: str, **kwargs):
        """Handle new tokens from the LLM."""
        result = ""
        for item in token:
            if item.get('type') and item['type'] == 'text':
                result += item['text']
            elif item.get('type') and item['type'] == 'tool_result':
                result += item['text']
            elif item.get('type'):
                result += f"Unknown token type: {item.get('type')} and item='{item}'"
        print(result, end="", flush=True)

    def on_llm_end(self, response, **kwargs):
        """Handle the end of an LLM thought."""
        print()  # Move to the next line

    def on_llm_error(self, error, **kwargs):
        """Handle LLM errors."""
        print(f"  LLM error: {error}")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        """Handle the start of a tool execution."""
        tool_name = serialized["name"]
        print(f"• Using tool:\n{tool_name} with input: {input_str}\n")

    def on_tool_end(self, output, **kwargs):
        """Handle the end of a tool execution."""
        print(f"    Tool output:\n{output}")

    def on_tool_error(self, error, **kwargs):
        """Handle tool errors."""
        print(f"    Tool error:\n{error}")

    def on_agent_finish(self, finish, **kwargs):
        """Handle the final output of the agent."""
        pass
        # result = finish.return_values
        # final_output = "\n".join(item['text'] for item in result["output"])
        # print(f"• Final answer: {final_output}")

import warnings
from langchain._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_executor = get_agent(option=MODEL_SONNET_37, memory=memory, streaming=True, converse_chat=True, thinking=False)

def run_agent_example(query) -> dict:
    print(f"\n--- Running agent with query: '{query}' ---")
    result = agent_executor.invoke({"input": query})
    return result

# Convert to interactive chatbot
print("\n=== Interactive Agent Chatbot ===")
print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")

while True:
    user_input = input("You: ")
    
    # Check for exit commands
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break
        
    # Process the user input through the agent
    try:
        callback_handler = ConsoleCallbackHandler()
        result = agent_executor.invoke({"input": user_input}, {"callbacks": [callback_handler]})   
        print()         
    except Exception as e:
        print(f"\nError: {str(e)}")