# A basic cli agent
This example demonstrates a simple command-line agent using LangChain. Let's break down the key components and address some important considerations:

1.  **Warning Suppression:**

    ```python
    import warnings
    from langchain._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
    ```

    This section disables deprecation warnings specifically related to LangChain.  This is generally done to prevent the console from being flooded with warnings about features that might change in future versions. While convenient for cleaner output, be aware that suppressing warnings might hide important information about potential compatibility issues down the line.  It's often better to address the warnings directly by updating the code to use the recommended, non-deprecated methods.

2.  **Agent Initialization and `AgentType`:**

    The code initializes a conversational agent.  A crucial aspect here is the `AgentType`.  Different `AgentType` enums in LangChain have different capabilities and limitations. Some agent types, particularly those designed for structured chat or function calling, might not inherently support conversational memory. This is because their underlying prompts and mechanisms are not designed to handle a continuous exchange of messages. The `AgentType` used here might not be compatible with the `ConversationBufferMemory`.

3.  **Memory (Conversation History):**

    ```python
    from langchain.memory import ConversationBufferMemory
    ```

    `ConversationBufferMemory` is used to store the conversation history. This allows the agent to "remember" past interactions and provide contextually relevant responses. However, as mentioned above, the chosen `AgentType` must be compatible with this memory mechanism. If the agent type doesn't explicitly support incorporating chat history into its prompts, the memory might not be used effectively, or might even cause errors. The prompt needs to support a variable like `chat_history` or `history`.

4. **Tool usage**
    The agent is not correctly using the tool. It seems to inject the tool output as a string, and not use the schema.

## Problem
The problem what this agent has is that it does not support multi-input tools, and that it does something weird with the tool. It looks like in injects a string, but we state the schema in the @tool decorator.

Here is the conversation. I ask it to do 40 times 2, but the tool response is 4040, but the python expression is return a * 2, which means that a is of type string and not of type int, but the tool defines the type as int. So the agent does not use the schema.

## Output

```
(study-streamlit-langchain-agent) ➜  study-streamlit-langchain-agent python main.py                                    
You: Hi chat
Hi Dennis! It's nice to see you again. How can I help you today?
You: What tools do you know?
Hi Dennis! I have access to one tool:

times_two: This tool takes a number as input and returns twice that number. It's a simple multiplication tool that always gives the correct result.

Is there something specific you'd like me to help you with using this tool, or do you have other questions?
```
You: do 40 times 2
I used the times_two tool to calculate 40 times 2, and the result is 80.

Wait - I notice there seems to be an issue with the tool output I received, which showed "4040" instead of the expected 80. This appears to be a formatting error where the input (40) was concatenated with the expected result (40) rather than performing multiplication.

The correct answer for 40 times 2 is 80.
```
You:
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

# disable warnings
import warnings
from langchain._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# set up the model
model_arn = "arn:aws:bedrock:us-east-1:015242279314:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
max_tokens = 100000
temperature = 0

session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime', 'us-east-1')

# Create the base Claude model
claude_bedrock = ChatBedrock(
                  model_id=model_id,
                  provider="anthropic",
                  client=bedrock_client,
                  model_kwargs={
                      "temperature": temperature, 
                      "max_tokens": max_tokens,                      
                  },
                  streaming=True,
)

# setup tools
@tool
def add(a: int, b: int) -> int:
    """Adds a and b and returns the result as a number. The response is always correct."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b and returns the result as a number. The response is always correct."""
    return a * b

@tool
def times_two(a: int) -> int:
    """Accepts a number and returns twice that number. The response is always correct."""
    return a * 2


memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True,
)

agent_executor = initialize_agent(
        tools=[times_two],
        llm=claude_bedrock,
        # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, # does not have memory
        # agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, # does not support multi-import tools, but has memory
        # agent=AgentType.OPENAI_MULTI_FUNCTIONS, # functions: Extra inputs are not permitted
        # agent=AgentType.OPENAI_FUNCTIONS, # functions: Extra inputs are not permitted
        # agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, # does not support multi-import tools, but has memory
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, # ChatAgent does not support multi-input tool add.        
        verbose=False,
        memory=memory,    
)

# setup history
test_history = [
    {"role": "human", "content": "Hi chat, my name is Dennis"},
    {
        "role": "ai",
        "content": (
            "Hi Dennis, I'm a chatbot. I'm here to help you with any questions you have. "
        ),
    },
]

# add history to memory
for msg in test_history:
    memory.chat_memory.add_message(
        (
            HumanMessage(content=msg["content"])
            if msg["role"] == "human"
            else AIMessage(content=msg["content"])
        )
    )

# start the chat
while True:
    user_input = input("You: ")
    response = agent_executor.invoke(
        input=user_input,
    )
    print(response["output"])
```
