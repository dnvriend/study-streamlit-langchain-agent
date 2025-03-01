# Tool calling
Source: https://python.langchain.com/docs/concepts/tool_calling/

# Overview
Many AI applications interact directly with humans. In these cases, it is appropriate for models to respond in natural language. But what about cases where we want a model to also interact directly with systems, such as databases or an API? These systems often have a particular input schema; for example, APIs frequently have a required payload structure. This need motivates the concept of tool calling. You can use tool calling to request model responses that match a particular schema.

> info: You will sometimes hear the term function calling. We use this term interchangeably with tool calling.

# Conceptual overview of tool calling

## Key concepts
(1) Tool Creation: Use the @tool decorator to create a tool. A tool is an association between a function and its schema. (2) Tool Binding: The tool needs to be connected to a model that supports tool calling. This gives the model awareness of the tool and the associated input schema required by the tool. (3) Tool Calling: When appropriate, the model can decide to call a tool and ensure its response conforms to the tool's input schema. (4) Tool Execution: The tool can be executed using the arguments provided by the model.

## Conceptual parts of tool calling

## Recommended usage
This pseudo-code illustrates the recommended workflow for using tool calling. Created tools are passed to .bind_tools() method as a list. This model can be called, as usual. If a tool call is made, model's response will contain the tool call arguments. The tool call arguments can be passed directly to the tool.

```python
# Tool creation
tools = [my_tool]
# Tool binding
model_with_tools = model.bind_tools(tools)
# Tool calling 
response = model_with_tools.invoke(user_input)
```

## Tool creation
The recommended way to create a tool is using the @tool decorator.

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b
```

## Tool binding
Many model providers support tool calling.

> tip: See our model integration page for a list of providers that support tool calling.

The central concept to understand is that LangChain provides a standardized interface for connecting tools to models. The .bind_tools() method can be used to specify which tools are available for a model to call.

```python
model_with_tools = model.bind_tools(tools_list)
```
As a specific example, let's take a function multiply and bind it as a tool to a model that supports tool calling.

```python
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = tool_calling_model.bind_tools([multiply])
```

## Tool calling
Diagram of a tool call by a model

A key principle of tool calling is that the model decides when to use a tool based on the input's relevance. The model doesn't always need to call a tool. For example, given an unrelated input, the model would not call the tool:

```python
result = llm_with_tools.invoke("Hello world!")
```

The result would be an AIMessage containing the model's response in natural language (e.g., "Hello!"). However, if we pass an input relevant to the tool, the model should choose to call it:

```python
result = llm_with_tools.invoke("What is 2 multiplied by 3?")
```

As before, the output result will be an AIMessage. But, if the tool was called, result will have a tool_calls attribute. This attribute includes everything needed to execute the tool, including the tool name and input arguments:

```python
result.tool_calls
{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'xxx', 'type': 'tool_call'}
```

For more details on usage, see our how-to guides!

## Tool execution
Tools implement the Runnable interface, which means that they can be invoked (e.g., tool.invoke(args)) directly.

LangGraph offers pre-built components (e.g., ToolNode) that will often invoke the tool in behalf of the user.


## Comments

model_with_tools = model.bind_tools([tools_list])

it seems like bind_tools requires list of list. I guess this might be better:
model_with_tools = model.bind_tools(tools_list)


1

🚀
1
3 replies
@thomasthm
thomasthm
Nov 14, 2024
True

@Bhargav2525
Bhargav2525
Dec 13, 2024
model_with_tools = model.bind_tools(tools_list) this means we have to pass list containing tools into model
Ex:- model_with_tools = model.bind_tools([multiply,add,....])

bind_tools will take list only not list of list


👍
1
@mcavdar
mcavdar
Dec 13, 2024
it was fixed in https://github.com/langchain-ai/langchain/pull/28222/files

@smithlai
smithlai
Dec 25, 2024
## tool 1:
tavily_search_tool = TavilySearchResults(max_results=2)
## tool 2:
from langchain_core.tools import tool
@tool(name_or_callable="magic_words")
def magic_words(username: str) -> str:
    """answer a dynamic password if user want to know magic words
    
    Args:
        username: name of user, or "<UNKNOWN>" if you don't know the username.
    """
    mw = "xxxxxxxxxx" + username
    print(mw)
    return mw

## tool 3
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b
    
# -----
tools = [tavily_search_tool, magic_words, multiply]
llm_with_tools = llm.bind_tools(tools)

I can get currect result with tavily_search
but I can't correctly run with my customized tools:

User: what is 2 * 18

{'chatbot': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_PvW9fA6mlYKvOtEgJ3sruwAB', 'function': {'arguments': '{"a":2,"b":18}', 'name': 'multiply'}, 'type': 'function'}]}, response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_d02d531b47'}, id='run-e8723c00-cb67-47e3-8b10-c3186c7395d0-0', tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 18}, 'id': 'call_PvW9fA6mlYKvOtEgJ3sruwAB', 'type': 'tool_call'}])]}}

{'mytools': {'messages': [ToolMessage(content='Error: multiply is not a valid tool, try one of [tool].', name='multiply', id='21592e88-dbc8-4145-b79f-24ea79e8bad3', tool_call_id='call_PvW9fA6mlYKvOtEgJ3sruwAB', status='error')]}}
DBG: content='' additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_v51wDdcXk4LezEpU7Mnabqvy', 'function': {'arguments': '{"a":2,"b":18}', 'name': 'multiply'}, 'type': 'function'}]} response_metadata={'finish_reason': 'tool_calls', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_d02d531b47'} id='run-c159e91b-c86d-43e3-9402-f64d54d1931e-0' tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 18}, 'id': 'call_v51wDdcXk4LezEpU7Mnabqvy', 'type': 'tool_call'}]

is anything wrong?


1
2 replies
@smithlai
smithlai
Dec 25, 2024
Well, it's my fault.
I forgot to update the tools node .

graph_builder.add_node("mytools", ToolNode(tools=tools))

@Keerthivardhan1
Keerthivardhan1
29 days ago
But it should work right ? what is wrong in initial code
we need to bind the tool to llm thats it, and you did it .

@HamzaRaouf
HamzaRaouf
Jan 2
edited
can we bind tools with hugging face model ?, whic is load like
model = AutoModelForCausalLM.from_pretrained(f"cache1/model/{model_id}").to(device)

I'm using HuggingFace model


1
0 replies
@daniyalk20
daniyalk20
Jan 23
Can we call another tool from another tool that is defined in the same stategraph?