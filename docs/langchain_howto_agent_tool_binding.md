# Langchain How-To: Agent Tool Binding

This document explains how to create an agent in LangChain that uses tool binding, specifically with AWS Bedrock and Anthropic's Claude models. It highlights the differences in tool-calling behavior between Claude 3.5 Sonnet v1, Claude 3.5 Sonnet v2, and Claude 3.7 Sonnet.

## Code Explanation

The provided Python code demonstrates how to build a simple mathematical agent capable of performing addition and multiplication by two. Here's a breakdown:

1.  **Tool Definition (using `@tool` decorator):**

    ```python
    from langchain_core.tools import tool

    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers together and return the result."""
        return a + b

    @tool
    def times_two(a: int) -> int:
        """Multiply a number by two and return the result."""
        return a * 2
    ```

    -   The `@tool` decorator from `langchain_core.tools` is used to define the functions `add` and `times_two` as tools. This decorator automatically handles the creation of the necessary tool schema, simplifying the process compared to manually defining Pydantic models. This is the preferred, simpler way to define tools.

2.  **AWS Bedrock Client and Model Setup:**

    ```python
    import boto3
    from langchain_aws import ChatBedrockConverse

    session = boto3.Session(region_name="us-east-1")
    bedrock_client = session.client('bedrock-runtime')

    model = ChatBedrockConverse(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        client=bedrock_client,
        temperature=0,
        max_tokens=1000
    )
    ```

    -   This section sets up the connection to AWS Bedrock and initializes the Claude language model (Claude 3.7 Sonnet in this example, but the code also shows how to use 3.5 Sonnet).  The `ChatBedrockConverse` class from `langchain_aws` is used.  Key parameters include `temperature` (controlling randomness) and `max_tokens` (limiting response length).

3.  **Prompt Template:**

    ```python
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that is good at math..."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    ```

    -   A `ChatPromptTemplate` is defined to structure the conversation with the model.  Crucially, it includes:
        -   A system message setting the agent's role.
        -   `MessagesPlaceholder` for `chat_history`: This enables conversational memory.
        -   A human message placeholder for the user's input (`{input}`).
        -   `MessagesPlaceholder` for `agent_scratchpad`:  This is essential for the agent to keep track of its intermediate reasoning steps and tool invocations.

4.  **Memory Setup:**

    ```python
    from langchain.memory import ConversationBufferMemory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    ```

    -   `ConversationBufferMemory` is used to store the conversation history.  `memory_key="chat_history"` links it to the `chat_history` placeholder in the prompt. `return_messages=True` ensures that the memory is returned as a list of messages, which is suitable for chat models.

5.  **Agent Creation ( `create_tool_calling_agent` ):**

    ```python
    from langchain.agents import create_tool_calling_agent
    tools = [add, times_two]
    agent = create_tool_calling_agent(model, tools, prompt)
    ```

    -   This is the core of the agent creation.  `create_tool_calling_agent` from `langchain.agents` is a function specifically designed for models that support tool calling (like Claude 3.5 Sonnet and 3.7 Sonnet).  It takes the language model (`model`), the list of tools (`tools`), and the prompt (`prompt`) as input.  This function handles the complex logic of binding the tools to the model and setting up the agent's internal reasoning process.

6.  **Agent Executor:**

    ```python
    from langchain.agents import AgentExecutor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
    ```

    -   The `AgentExecutor` wraps the agent and provides the runtime environment.  It takes the `agent`, the `tools`, and the `memory` as input.  `verbose=True` enables detailed logging of the agent's actions, which is very helpful for debugging.

7.  **Running the Agent:**

    ```python
    def run_agent_example(query) -> dict:
        print(f"\n--- Running agent with query: '{query}' ---")
        result = agent_executor.invoke({"input": query})
        return result

    x = run_agent_example("What's 15 plus 27?")
    y = run_agent_example("Can you double the number 40?")
    z = run_agent_example("What was the result of the first calculation I asked you to do?")
    ```

    -   The `agent_executor.invoke()` method is used to interact with the agent.  The input is provided as a dictionary with the key `"input"`, matching the `"{input}"` placeholder in the prompt. The agent executor handles passing the input to the agent, managing the conversation history, invoking tools, and returning the final result.

## Model Comparison (Claude 3.5 Sonnet v1, v2, and 3.7 Sonnet)

The output logs demonstrate significant differences in how the different Claude versions handle tool calling:

*   **Claude 3.5 Sonnet v1:**  While it *attempts* to use the tools (as seen in the `Invoking: add` log), it *also* generates text that tries to answer the question directly *before* making the tool call. This indicates less reliable tool use. It gets the correct answer, but it's not strictly following the tool-calling protocol. It also hallucinates the response format, including both `text` and `tool_use` in the response, when it should only include `tool_use`.

*   **Claude 3.5 Sonnet v2 and Claude 3.7 Sonnet:** These versions show *much* improved tool-calling behavior. The logs clearly show the agent correctly invoking the `add` and `times_two` tools with the appropriate arguments.  The agent *only* outputs the tool invocation and *doesn't* try to answer the question directly in the text. This demonstrates that the agent is correctly delegating the calculation to the tools. The response format is also correct, only including the `tool_use` information.

The key takeaway is that Claude 3.5 Sonnet v2 and Claude 3.7 Sonnet exhibit significantly more reliable and accurate tool-calling behavior compared to v1. This aligns with Anthropic's announcements regarding improved function calling capabilities in the newer models. The agent, when using these later models, correctly uses the tools to perform the calculations and relies on the tool output for the final answer.


## Output of Claude 3.5 Sonnet v1

```
--- Running agent with query: 'What's 15 plus 27?' ---


> Entering new AgentExecutor chain...

Invoking: `add` with `{'a': 15, 'b': 27}`
responded: [{'type': 'text', 'text': 'To answer this question, I can use the "add" function that\'s available to me. Let me calculate that for you.', 'index': 0}, {'type': 'tool_use', 'name': 'add', 'id': 'tooluse_oxdMU_dXRSOBMbhIet_62Q', 'index': 1, 'input': '{"a": 15, "b": 27}'}]

42[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is 42.\n\nSo, 15 plus 27 equals 42.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'Can you double the number 40?' ---


> Entering new AgentExecutor chain...

Invoking: `times_two` with `{'a': 40}`
responded: [{'type': 'text', 'text': 'Certainly! I can use the "times_two" function to double the number 40 for you. Let me do that calculation.', 'index': 0}, {'type': 'tool_use', 'name': 'times_two', 'id': 'tooluse_dwIbIbtTSWKdi3Wbal8w1A', 'index': 1, 'input': '{"a": 40}'}]

80[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.\n\nSo, when we double the number 40, we get 80 as the answer.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'What was the result of the first calculation I asked you to do?' ---


> Entering new AgentExecutor chain...

Invoking: `add` with `{'a': 15, 'b': 27}`
responded: [{'type': 'text', 'text': 'I apologize for the confusion in my previous responses. I realize now that I didn\'t actually perform the calculations using the available tools. Let me correct that and provide you with the accurate information using the appropriate function calls.\n\nFor your first question, "What\'s 15 plus 27?", let\'s use the "add" function to calculate the result:', 'index': 0}, {'type': 'tool_use', 'name': 'add', 'id': 'tooluse_HXB11v6hRNGGyqUd6f59jQ', 'index': 1, 'input': '{"a": 15, "b": 27}'}]

42[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is indeed 42.\n\nTo answer your current question about the result of the first calculation: The result of 15 plus 27 was 42.\n\nI apologize for not using the tool initially. Thank you for bringing this to my attention, as it allows me to provide you with the correct information using the available functions.', 'index': 0}]

> Finished chain.
x: {'input': "What's 15 plus 27?", 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is 42.\n\nSo, 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.\n\nSo, when we double the number 40, we get 80 as the answer.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is indeed 42.\n\nTo answer your current question about the result of the first calculation: The result of 15 plus 27 was 42.\n\nI apologize for not using the tool initially. Thank you for bringing this to my attention, as it allows me to provide you with the correct information using the available functions.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is 42.\n\nSo, 15 plus 27 equals 42.', 'index': 0}]}

y: {'input': 'Can you double the number 40?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is 42.\n\nSo, 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.\n\nSo, when we double the number 40, we get 80 as the answer.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is indeed 42.\n\nTo answer your current question about the result of the first calculation: The result of 15 plus 27 was 42.\n\nI apologize for not using the tool initially. Thank you for bringing this to my attention, as it allows me to provide you with the correct information using the available functions.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.\n\nSo, when we double the number 40, we get 80 as the answer.', 'index': 0}]}

z: {'input': 'What was the result of the first calculation I asked you to do?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is 42.\n\nSo, 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.\n\nSo, when we double the number 40, we get 80 as the answer.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is indeed 42.\n\nTo answer your current question about the result of the first calculation: The result of 15 plus 27 was 42.\n\nI apologize for not using the tool initially. Thank you for bringing this to my attention, as it allows me to provide you with the correct information using the available functions.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe result of adding 15 and 27 is indeed 42.\n\nTo answer your current question about the result of the first calculation: The result of 15 plus 27 was 42.\n\nI apologize for not using the tool initially. Thank you for bringing this to my attention, as it allows me to provide you with the correct information using the available functions.', 'index': 0}]}
```

## Output of Claude 3.5 Sonnet v2

```
--- Running agent with query: 'What's 15 plus 27?' ---


> Entering new AgentExecutor chain...

Invoking: `add` with `{'a': 15, 'b': 27}`
responded: [{'type': 'text', 'text': 'I can help you add those numbers together using the `add` function.', 'index': 0}, {'type': 'tool_use', 'name': 'add', 'id': 'tooluse_gHLkkpvxQM61IcIRacvtIg', 'index': 1, 'input': '{"a": 15, "b": 27}'}]

42[{'type': 'text', 'text': '\n\n15 plus 27 equals 42.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'Can you double the number 40?' ---


> Entering new AgentExecutor chain...

Invoking: `times_two` with `{'a': 40}`
responded: [{'type': 'text', 'text': "I'll use the times_two function to multiply 40 by 2.", 'index': 0}, {'type': 'tool_use', 'name': 'times_two', 'id': 'tooluse_rjRxArn8RXqH7lkh_sOR0Q', 'index': 1, 'input': '{"a": 40}'}]

80[{'type': 'text', 'text': '\n\n40 doubled equals 80.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'What was the result of the first calculation I asked you to do?' ---


> Entering new AgentExecutor chain...

Invoking: `add` with `{'a': 15, 'b': 27}`
responded: [{'type': 'text', 'text': 'In your first question, you asked what 15 plus 27 is. Let me calculate that again:', 'index': 0}, {'type': 'tool_use', 'name': 'add', 'id': 'tooluse_eB5dnV2TR26q9ICdYh2jWw', 'index': 1, 'input': '{"a": 15, "b": 27}'}]

42[{'type': 'text', 'text': '\n\nThe result was 42.', 'index': 0}]

> Finished chain.
x: {'input': "What's 15 plus 27?", 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n40 doubled equals 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\n15 plus 27 equals 42.', 'index': 0}]}

y: {'input': 'Can you double the number 40?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n40 doubled equals 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\n40 doubled equals 80.', 'index': 0}]}

z: {'input': 'What was the result of the first calculation I asked you to do?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\n40 doubled equals 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe result was 42.', 'index': 0}]}
```

## Output of Claude 3.7 Sonnet

```
--- Running agent with query: 'What's 15 plus 27?' ---


> Entering new AgentExecutor chain...

Invoking: `add` with `{'a': 15, 'b': 27}`
responded: [{'type': 'text', 'text': 'I can help you calculate 15 plus 27 using the addition tool.', 'index': 0}, {'type': 'tool_use', 'name': 'add', 'id': 'tooluse_iffOXP_1TZC6lkHtRyYx3Q', 'index': 1, 'input': '{"a": 15, "b": 27}'}]

42[{'type': 'text', 'text': '\n\nThe sum of 15 plus 27 equals 42.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'Can you double the number 40?' ---


> Entering new AgentExecutor chain...

Invoking: `times_two` with `{'a': 40}`
responded: [{'type': 'text', 'text': 'I can help you double the number 40 using the times_two function.', 'index': 0}, {'type': 'tool_use', 'name': 'times_two', 'id': 'tooluse_uKW8fxSJSp2Ur6Xxh3mdoQ', 'index': 1, 'input': '{"a": 40}'}]

80[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.', 'index': 0}]

> Finished chain.

--- Running agent with query: 'What was the result of the first calculation I asked you to do?' ---


> Entering new AgentExecutor chain...
[{'type': 'text', 'text': 'The first calculation you asked me to do was 15 plus 27, and the result was 42.', 'index': 0}]

> Finished chain.
x: {'input': "What's 15 plus 27?", 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe sum of 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': 'The first calculation you asked me to do was 15 plus 27, and the result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe sum of 15 plus 27 equals 42.', 'index': 0}]}

y: {'input': 'Can you double the number 40?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe sum of 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': 'The first calculation you asked me to do was 15 plus 27, and the result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.', 'index': 0}]}

z: {'input': 'What was the result of the first calculation I asked you to do?', 'chat_history': [HumanMessage(content="What's 15 plus 27?", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe sum of 15 plus 27 equals 42.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='Can you double the number 40?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': '\n\nThe result of doubling 40 is 80.', 'index': 0}], additional_kwargs={}, response_metadata={}), HumanMessage(content='What was the result of the first calculation I asked you to do?', additional_kwargs={}, response_metadata={}), AIMessage(content=[{'type': 'text', 'text': 'The first calculation you asked me to do was 15 plus 27, and the result was 42.', 'index': 0}], additional_kwargs={}, response_metadata={})], 'output': [{'type': 'text', 'text': 'The first calculation you asked me to do was 15 plus 27, and the result was 42.', 'index': 0}]}
```

## Code

```python
from langchain_aws import ChatBedrockConverse
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
import boto3

# disable warnings
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


tools = [add, times_two]

# 4. Set up AWS Bedrock client
session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime')

# 5. Initialize the Claude 3.7 Sonnet model
model = ChatBedrockConverse(
    # model="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    client=bedrock_client,
    temperature=0,
    max_tokens=1000
)

# 6. Create a prompt template for the agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that is good at math. You have access to tools that can help you perform calculations."),
    MessagesPlaceholder(variable_name="chat_history"),  # For memory
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")  # For agent reasoning
])

# 7. Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 8. Create the agent using create_tool_calling_agent
agent = create_tool_calling_agent(model, tools, prompt)

# 9. Wrap the agent in an AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)

# 10. Run some examples
def run_agent_example(query) -> dict:
    print(f"\n--- Running agent with query: '{query}' ---")
    result = agent_executor.invoke({"input": query})
    return result

x = run_agent_example("What's 15 plus 27?")
y = run_agent_example("Can you double the number 40?")
z = run_agent_example("What was the result of the first calculation I asked you to do?")    

print(f"x: {x}\n")
print(f"y: {y}\n")
print(f"z: {z}\n")
```

