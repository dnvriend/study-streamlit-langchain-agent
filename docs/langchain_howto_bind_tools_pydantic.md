# How to bind tools using Pydantic

This example demonstrates how to define and bind custom tools to a language model (specifically, Anthropic's Claude 3.5 Sonnet on AWS Bedrock) using LangChain, with a focus on using Pydantic for schema definition.  The tools allow the model to perform addition and multiplication by two.

1.  **Tool Schema Definition (Pydantic Models):**

    *   Pydantic models `AddTool` and `TimesTwoTool` are defined to specify the structure of each tool's input.  This is crucial for ensuring the model provides arguments in the correct format.
    *   Each model defines its input fields (e.g., `a` and `b` for `AddTool`, `a` for `TimesTwoTool`) along with their types (`int`) and descriptions.  The descriptions are important for guiding the model on how to use the tool.
    *   Using Pydantic models provides strong typing and validation, making the interaction with the tools more robust.

2.  **Tool Implementation (Functions):**

    *   The `add(a: int, b: int) -> int` and `times_two(a: int) -> int` functions are the actual implementations of the tools.  They take integers as input and return the result of the respective operation.  These are standard Python functions.

3.  **Bedrock Client Setup:**

    *   The code sets up a connection to AWS Bedrock using `boto3`.  This is necessary to interact with the Claude model hosted on Bedrock.

4.  **Model Initialization:**

    *   `ChatBedrockConverse` initializes the Claude 3.5 Sonnet model. Key parameters:
        *   `model`:  Specifies the exact model version. Note the use of `claude-3-5-sonnet`.
        *   `client`: The Bedrock client.
        *   `temperature`: Controls randomness (0 for deterministic output).
        *   `max_tokens`:  Limits response length.

5.  **Tool Binding:**

    *   `model.bind_tools(tools)` is the key step where the defined tools are associated with the language model.
    *   The `tools` list contains a dictionary for each tool:
        *   `name`: The tool's name (used by the model).
        *   `description`:  Explains what the tool does.
        *   `input_schema`: The JSON schema *generated from the Pydantic model*.  This is how the model knows the expected input format.  `AddTool.model_json_schema()` and `TimesTwoTool.model_json_schema()` automatically create the JSON schema from the Pydantic class definitions.

6.  **Model Invocation and Tool Use:**

    *   `model_with_tools.invoke(query)` sends the user's query to the model.  The model, having been bound to the tools, can now recognize when a query requires their use.
    *   The response will be an `AIMessage` object.  If the model decides to use a tool, the `tool_calls` attribute of this object will be populated.  It *won't* directly answer the query in text.
    *   `tool_calls` is a list of dictionaries, each representing a tool call:
        *   `name`: The name of the tool to call.
        *   `args`:  A dictionary of arguments to pass to the tool.  The keys and value types in this dictionary *must* match the `input_schema` defined earlier.

7.  **Tool Execution and Result:**

    *   The code checks for `tool_calls`.  If present, it extracts the tool name and arguments.
    *   It then dynamically calls the correct function (`add` or `times_two`) using `globals()[tool_call['name']](**tool_call['args'])`.  This is a way to call a function by its name (which is a string).
    *   The result of the tool's execution is then printed.

8. **Debugging the output:**
    * The `process_query` function is used to debug the output.
    * It prints the query, the response type, and whether a tool call is present.
    * If a tool call is present, it prints the tool name and arguments.
    * It then calls the tool and prints the result.
    * If no tool was called, it prints the model's response.

# Code

```python
from pydantic import BaseModel, Field
from typing import List
from langchain_aws import ChatBedrockConverse
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

class TimesTwoTool(BaseModel):
    """Multiply a number by two and return the result."""
    a: int = Field(..., description="Number to multiply by two")

def times_two(a: int) -> int:
    """Multiply a number by two and return the result."""
    return a * 2

# 3. Set up AWS Bedrock client
session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime')

# 4. Initialize the Claude 3.7 Sonnet model
model = ChatBedrockConverse(
    model="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
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
    },
    {
        "name": "times_two",
        "description": "Multiply a number by two and return the result.",
        "input_schema": TimesTwoTool.model_json_schema()
    }
]
model_with_tools = model.bind_tools(tools)

def process_query(query):
    print(f"Processing query: {query}")
    
    # Invoke the model with a request that should trigger tool use
    response = model_with_tools.invoke(query)

    print(f"Response type: {type(response)}")
    print(f"Is tool call present? {'tool_calls' in dir(response)}")

    if hasattr(response, 'tool_calls') and response.tool_calls:
        # Extract the tool call details - treating tool_call as a dictionary
        tool_call = response.tool_calls[0]  # Get the first tool call
        
        # Handle tool_call as a dictionary
        print(f"\nTool called: {tool_call['name']}")
        print(f"Tool arguments: {tool_call['args']}")
                
        result = globals()[tool_call['name']](**tool_call['args'])
        print(f"\nComputation result: {result}")
        return result
    else:
        print("\nNo tool was called. Model response:")
        return response.content

process_query("What's 15 plus 27?")    
process_query("Double the number 40.")     
```