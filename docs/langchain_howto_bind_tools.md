# How to bind tools to a model
This code demonstrates how to define and bind a custom tool to a language model (specifically, Anthropic's Claude 3.7 Sonnet on AWS Bedrock) using LangChain. The tool allows the model to perform addition. Let's break down the key parts:

1.  **Tool Schema Definition (Pydantic Model):**
    *   A Pydantic model `AddTool` is defined to specify the structure of the tool's input. This acts as a schema, ensuring the model provides arguments in the correct format. It defines two integer fields, `a` and `b`, with descriptions.

2.  **Tool Implementation (Function):**
    *   The `add(a: int, b: int) -> int` function is the actual implementation of the tool. It takes two integers as input and returns their sum. This is the code that gets executed when the model decides to use the tool.

3.  **Bedrock Client Setup:**
    *   The code sets up a connection to AWS Bedrock, which is a service that provides access to various foundation models, including Claude.

4.  **Model Initialization:**
    *   `ChatBedrockConverse` initializes the Claude 3.7 Sonnet model. Important parameters include:
        *   `model`: Specifies the exact model version.
        *   `client`: The Bedrock client.
        *   `temperature`: Controls the randomness of the model's output (0 for deterministic).
        *   `max_tokens`: Limits the maximum length of the response.

5.  **Tool Binding:**
    *   `model.bind_tools(tools)` is the crucial step. It associates the defined tool (`add`) with the language model. The `tools` list contains a dictionary describing the tool:
        *   `name`: The name of the tool (used by the model to refer to it).
        *   `description`: A description of what the tool does.
        *   `input_schema`: The JSON schema generated from the `AddTool` Pydantic model. This tells the model the expected input format for the tool.

6.  **Model Invocation and Tool Use:**
    *   `model_with_tools.invoke(user_query)` sends the user's query ("What's 15 plus 27?") to the model. Because the model has been bound to the `add` tool, it recognizes that this query requires addition.
    *   The response is an `AIMessage` object. Critically, instead of directly answering, the model returns a `tool_calls` attribute within the `AIMessage`. This attribute contains:
        *   `name`: The name of the tool to call (`add`).
        *   `args`: A dictionary of arguments to pass to the tool (`{'a': 15, 'b': 27}`).

7.  **Tool Execution and Result:**
    *   The code then checks for the presence of `tool_calls`. If present, it extracts the tool name and arguments.
    *   It calls the `add` function with the extracted arguments.
    *   The result of the tool execution (42) is printed.

8. **Interactive use**
    * The code can be used interactively by uncommenting the while loop.


## Output

```
python main.py               
Response type: <class 'langchain_core.messages.ai.AIMessage'>
Is tool call present? True

Tool called: add
Tool arguments: {'a': 15, 'b': 27}

Computation result: 42
```

## Code

```python
from calculating_tools import times_two
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_aws import ChatBedrock
import boto3
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import AIMessage
import boto3

# disable warnings
import warnings
from langchain._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)


# 1. Define tool schema using Pydantic
class AddTool(BaseModel):
    """Add two numbers together."""
    a: int = Field(..., description="First number to add")
    b: int = Field(..., description="Second number to add")

# 2. Implementation of the actual function
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    return a + b

# 3. Set up AWS Bedrock client 
session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime')

# 4. Initialize the Claude 3.7 Sonnet model
model = ChatBedrockConverse(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    client=bedrock_client,
    temperature=0,
    max_tokens=1000
)

# 5. Bind the tool to the model
tools = [
    {
        "name": "add",
        "description": "Add two numbers together.",
        "input_schema": AddTool.model_json_schema()
    }
]
model_with_tools = model.bind_tools(tools)

# 6. Invoke the model with a request that should trigger tool use
user_query = "What's 15 plus 27?"
response = model_with_tools.invoke(user_query)

print(f"Response type: {type(response)}")
print(f"Is tool call present? {'tool_calls' in dir(response)}")

if hasattr(response, 'tool_calls') and response.tool_calls:
    # Extract the tool call details
    tool_call = response.tool_calls[0]
    print(f"\nTool called: {tool_call['name']}")
    print(f"Tool arguments: {tool_call['args']}")
    
    # Execute the tool with the provided arguments
    if tool_call['name'] == "add":
        result = add(**tool_call['args'])
        print(f"\nComputation result: {result}")
else:
    print("\nNo tool was called. Model response:")
    print(response.content)
```