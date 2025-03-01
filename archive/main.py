from langchain_aws import ChatBedrockConverse
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_community.tools import ShellTool
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
import boto3

import warnings
from langchain._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    return a + b

@tool
def times_two(a: int) -> int:
    """Multiply a number by two and return the result."""
    return a * 2

# Create shell tool
shell_tool = ShellTool()
shell_tool.description = """
Use this tool to execute bash commands on the Linux operating system.
The input should be a valid bash command.
For listing files, use: ls -la
For checking the current directory, use: pwd
For reading file contents, use: cat filename
"""

# Create Python REPL tool
python_tool = PythonREPLTool()
python_tool.description = """
A Python shell. Use this to execute Python code. 
Input should be a valid Python command. 
If you want to see the output of a value, you should print it out with `print(...)`.
Example: To calculate the area of a circle with radius 2, use:
```python
import math
radius = 2
area = math.pi * (radius ** 2)
print(area)
```
"""

requests_toolkit = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True,
)

# Add all tools to the tools list
tools = [add, times_two, shell_tool, python_tool]
# Extend the tools list with the toolkit's tools
tools.extend(requests_toolkit.get_tools())

session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime')

model = ChatBedrockConverse(
    # model="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    client=bedrock_client,
    temperature=0,
    max_tokens=1000
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that is good at math, can interact with the file system, "
              "and can execute Python code. You have access to tools that can help you perform calculations, "
              "execute shell commands, and run Python code. When asked to solve problems using Python, "
              "use the Python REPL tool. When asked to interact with files, use the shell tool."),
    MessagesPlaceholder(variable_name="chat_history"),  # For memory
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")  # For agent reasoning
])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, memory=memory)

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
        result = agent_executor.invoke({"input": user_input})
        print("\nAssistant:", "\n".join(item['text'] for item in result["output"]))
    except Exception as e:
        print(f"\nError: {str(e)}")
        
