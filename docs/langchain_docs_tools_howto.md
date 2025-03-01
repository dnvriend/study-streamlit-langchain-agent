# How to use chat models to call tools
Source: https://python.langchain.com/docs/how_to/tool_calling/

This guide assumes familiarity with the following concepts:

- Chat models: see docs/chat_models.md
- Tool calling: see docs/tool_calling.md
- Tools: see docs/tools.md 
- Output parsers: not applicable to us, we use ChatBedrock and Claude 3.5 Sonnet or Claude 3.7 Sonnet and they both support tool calling and structured output.

Tool calling allows a chat model to respond to a given prompt by "calling a tool".

## Model generate arguments to a tool
Remember, while the name "tool calling" implies that the model is directly performing some action, this is actually not the case! The model only generates the arguments to a tool, and actually running the tool (or not) is up to the user.

## Model generates structured output
Tool calling is a general technique that generates structured output from a model, and you can use it even when you don't intend to invoke any tools. An example use-case of that is extraction from unstructured text.

Diagram of calling a tool

If you want to see how to use the model-generated tool call to actually run a tool check out this guide.

Supported models
Tool calling is not universal, but is supported by many popular LLM providers. You can find a list of all models that support tool calling here.

LangChain implements standard interfaces for defining tools, passing them to LLMs, and representing tool calls. This guide will cover how to bind tools to an LLM, then invoke the LLM to generate these arguments.

Defining tool schemas
For a model to be able to call tools, we need to pass in tool schemas that describe what the tool does and what it's arguments are. Chat models that support tool calling features implement a .bind_tools() method for passing tool schemas to the model. Tool schemas can be passed in as Python functions (with typehints and docstrings), Pydantic models, TypedDict classes, or LangChain Tool objects. Subsequent invocations of the model will pass in these tool schemas along with the prompt.

Python functions
Our tool schemas can be Python functions:

# The function name, type hints, and docstring are all part of the tool
# schema that's passed to the model. Defining good, descriptive schemas
# is an extension of prompt engineering and is an important part of
# getting models to perform well.
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b

LangChain Tool
LangChain also implements a @tool decorator that allows for further control of the tool schema, such as tool names and argument descriptions. See the how-to guide here for details.

Pydantic class
You can equivalently define the schemas without the accompanying functions using Pydantic.

Note that all fields are required unless provided a default value.

from pydantic import BaseModel, Field


class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

TypedDict class
Requires langchain-core>=0.2.25
Or using TypedDicts and annotations:

from typing_extensions import Annotated, TypedDict


class add(TypedDict):
    """Add two integers."""

    # Annotations must have the type and can optionally include a default value and description (in that order).
    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


class multiply(TypedDict):
    """Multiply two integers."""

    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


tools = [add, multiply]


To actually bind those schemas to a chat model, we'll use the .bind_tools() method. This handles converting the add and multiply schemas to the proper format for the model. The tool schema will then be passed it in each time the model is invoked.

Select chat model:
pip install -qU "langchain[groq]"

import getpass
import os

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12?"

llm_with_tools.invoke(query)

AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_iXj4DiW1p7WLjTAQMRO0jxMs', 'function': {'arguments': '{"a":3,"b":12}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 80, 'total_tokens': 97}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_483d39d857', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-0b620986-3f62-4df7-9ba3-4595089f9ad4-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_iXj4DiW1p7WLjTAQMRO0jxMs', 'type': 'tool_call'}], usage_metadata={'input_tokens': 80, 'output_tokens': 17, 'total_tokens': 97})


As we can see our LLM generated arguments to a tool! You can look at the docs for bind_tools() to learn about all the ways to customize how your LLM selects tools, as well as this guide on how to force the LLM to call a tool rather than letting it decide.

Tool calls
If tool calls are included in a LLM response, they are attached to the corresponding message or message chunk as a list of tool call objects in the .tool_calls attribute.

Note that chat models can call multiple tools at once.

A ToolCall is a typed dict that includes a tool name, dict of argument values, and (optionally) an identifier. Messages with no tool calls default to an empty list for this attribute.

query = "What is 3 * 12? Also, what is 11 + 49?"

llm_with_tools.invoke(query).tool_calls

[{'name': 'multiply',
  'args': {'a': 3, 'b': 12},
  'id': 'call_1fyhJAbJHuKQe6n0PacubGsL',
  'type': 'tool_call'},
 {'name': 'add',
  'args': {'a': 11, 'b': 49},
  'id': 'call_fc2jVkKzwuPWyU7kS9qn1hyG',
  'type': 'tool_call'}]

The .tool_calls attribute should contain valid tool calls. Note that on occasion, model providers may output malformed tool calls (e.g., arguments that are not valid JSON). When parsing fails in these cases, instances of InvalidToolCall are populated in the .invalid_tool_calls attribute. An InvalidToolCall can have a name, string arguments, identifier, and error message.

Parsing
If desired, output parsers can further process the output. For example, we can convert existing values populated on the .tool_calls to Pydantic objects using the PydanticToolsParser:

from langchain_core.output_parsers import PydanticToolsParser
from pydantic import BaseModel, Field


class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


chain = llm_with_tools | PydanticToolsParser(tools=[add, multiply])
chain.invoke(query)

API Reference:PydanticToolsParser
[multiply(a=3, b=12), add(a=11, b=49)]

## Next steps
Now you've learned how to bind tool schemas to a chat model and have the model call the tool.

Next, check out this guide on actually using the tool by invoking the function and passing the results back to the model:

Pass tool results back to model
You can also check out some more specific uses of tool calling:

Getting structured outputs from models
Few shot prompting with tools
Stream tool calls
Pass runtime values to tools

# Questions about binding tools to a model

## Binding a Tool to a Model

### Question
Is it possible to use tools without using agents? As I understand it, there appears to be two ways to use tools: either with agents (seems to be the most common way) or, if you know you are going to be using a tool just once (or some specific number of times), you can use model.bind_tools() to 'bind' a tool to a model. For example, the following code should work:

```python
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import JsonOutputToolsParser
from langchain.output_parsers import JsonOutputKeyToolsParser
from operator import itemgetter

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

model = ChatOpenAI(model="gpt-3.5-turbo-1106")
model_with_tools = model.bind_tools([multiply], tool_choice="multiply")

# Note: the `.map()` at the end of `multiply` allows us to pass in a list of `multiply` arguments instead of a single one.
chain = (
    model_with_tools
    | JsonOutputKeyToolsParser(key_name="multiply", return_single=True)
    | multiply
)
chain.invoke("What's four times 23")
```

Ummm... what? It seems like we 'bound' the multiply tool to the model. There is a reference to .map() that I don't see in the code. We then proceed to chain it with a JSON Output Parser, and then... chain it to the multiply tool again? What does it mean to 'bind' a tool to a model anyways? Nowhere in the documentation is binding discussed in detail. Is the bound function always called? Sometimes called? If I bind multiple tools to a model, what does that mean?


### Answer
In LangChain, the concept of 'binding' a tool to a model refers to associating specific tools (like calculators, databases, etc.) with a language model so that the model can utilize these tools to perform tasks beyond its native capabilities. In your provided code, `model.bind_tools([multiply], tool_choice="multiply")` is binding the multiply tool to the ChatOpenAI model. This means that the model can now use the multiply tool to perform multiplication tasks. If you bind multiple tools to a model, the model will have access to all those tools and can use them as needed.

## Use of `load_tools()` Function

### Question
`load_tools()` is confusing: Where exactly are we supposed to find the names of the default tools to pass in as arguments to the load_tools function? For example, the following code works to give an agent the use of the OpenWeatherMap API:

```python
tools = load_tools(["openweathermap-api"])

# Agent and Agent Executor
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True)
```

### Answer
The load_tools() function is used to load the default tools provided by LangChain. The error you're encountering (ValueError: Got unknown tool DuckDuckGoSearchRun) suggests that DuckDuckGoSearchRun is not a recognized tool in the current version of LangChain you're using. It's possible that the tool name has changed or it's not included in the version you're using. Unfortunately, without access to the repository, I can't provide a list of the default tools. You might want to check the documentation or the source code of the load_tools() function to find the names of the default tools.

## Differences in binding tools: 

### Question
A myriad of ways to create agents: In addition to the load_tools template shown above, I have also seen the use of `initialize_agent`, which I believe is deprecated despite being littered all throughout the documentation. I have also seen `create_openai_tools_agent` used without load_tools:

```python
tools = [TavilySearchResults(max_results=1)]
prompt = hub.pull("hwchase17/openai-tools-agent")

# Choose the LLM that will drive the agent
# Only certain models support this
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)
```

How should I know if I need to be using load_tools or not? Subtle note, here we are using create_openai_tools_agent, before we used create_openai_functions_agent. I believe functions is deprecated, but again it is littered all throughout the documentation so I can't be sure.

### Answer
`load_tools`, `initialize_agent`, and `create_openai_tools_agent` methods are used for different purposes:

- `load_tools()`: This function is used to load the default tools provided by LangChain.
- `initialize_agent()`: This method is typically used to set up or initialize an agent with necessary configurations, models, or tools. However, without explicit reference in the provided code, its functionality or differences cannot be detailed.
- `create_openai_tools_agent()`: This method is used to create an agent that uses OpenAI tools alongside a language model. It binds the tools to the language model, sets up a processing pipeline that includes formatting tool messages, applying the prompt, processing with the language model, and parsing the output.


## Comments

useful doc, ^_^


1

❤️
1
0 replies
@lamoboos223
lamoboos223
Dec 21, 2024
amazing docs!

why tool calling isn't supported on llama3? i think it is the most important model among them all since it is open source and everyone can fine tune to there dataset.


1
1 reply
@Xx-AD16-xX
Xx-AD16-xX
Jan 12
Try using llama3 from groq and use it via chatgroq instead of using it locally; I have tried and it works!

@vivekatbitm
vivekatbitm
26 days ago
How can we pass methods of a class object, annotated as @tool. It's not working as first param of class instance methods is self. It complains while calling such tool method using .invoke call. For example: db_instance.get_students.invoke({}) fails saying
TypeError: StudentDB.get_students() missing 1 required positional argument: 'self'


1
0 replies
@gilbertorradecki
gilbertorradecki
2 days ago
I'm using the same code as above, except for the model: I'm using llama3-groq-tool-use 8B locally.
I'm wodering why I couldn't achieve the same result: when I pass two requests to my model, it only prints one of them:

query = "What is 3 * 12? Also and what is 11 + 49?"

chain = llm | PydanticToolsParser(tools=[multiply, add])

chain.invoke(query)

chain.invoke(query)

Out[81]: [multiply(a=3, b=12)]