# LangChain Docs: React Agent
Source: https://python.langchain.com/api_reference/langchain/agents/langchain.agents.react.agent.create_react_agent.html

create_react_agent
langchain.agents.react.agent.create_react_agent(llm: ~langchain_core.language_models.base.BaseLanguageModel, tools: ~typing.Sequence[~langchain_core.tools.base.BaseTool], prompt: ~langchain_core.prompts.base.BasePromptTemplate, output_parser: ~langchain.agents.agent.AgentOutputParser | None = None, tools_renderer: ~typing.Callable[[list[~langchain_core.tools.base.BaseTool]], str] = <function render_text_description>, *, stop_sequence: bool | ~typing.List[str] = True) → Runnable[source]
Create an agent that uses ReAct prompting.

Based on paper “ReAct: Synergizing Reasoning and Acting in Language Models” (https://arxiv.org/abs/2210.03629)

Warning

This implementation is based on the foundational ReAct paper but is older and not well-suited for production applications. For a more robust and feature-rich implementation, we recommend using the create_react_agent function from the LangGraph library. See the [reference doc](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent) for more information.

Parameters
:
llm (BaseLanguageModel) – LLM to use as the agent.

tools (Sequence[BaseTool]) – Tools this agent has access to.

prompt (BasePromptTemplate) – The prompt to use. See Prompt section below for more.

output_parser (AgentOutputParser | None) – AgentOutputParser for parse the LLM output.

tools_renderer (Callable[[list[BaseTool]], str]) – This controls how the tools are converted into a string and then passed into the LLM. Default is render_text_description.

stop_sequence (bool | List[str]) –

bool or list of str. If True, adds a stop token of “Observation:” to avoid hallucinates. If False, does not add a stop token. If a list of str, uses the provided list as the stop tokens.

Default is True. You may to set this to False if the LLM you are using does not support stop sequences.

Returns
:
A Runnable sequence representing an agent. It takes as input all the same input variables as the prompt passed in does. It returns as output either an AgentAction or AgentFinish.

Return type
:
Runnable

Examples

from langchain import hub
from langchain_community.llms import OpenAI
from langchain.agents import AgentExecutor, create_react_agent

prompt = hub.pull("hwchase17/react")
model = OpenAI()
tools = ...

agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_executor.invoke({"input": "hi"})

# Use with chat history
from langchain_core.messages import AIMessage, HumanMessage
agent_executor.invoke(
    {
        "input": "what's my name?",
        # Notice that chat_history is a string
        # since this prompt is aimed at LLMs, not chat models
        "chat_history": "Human: My name is Bob\nAI: Hello Bob!",
    }
)
Prompt:

The prompt must have input keys:
tools: contains descriptions and arguments for each tool.

tool_names: contains all tool names.

agent_scratchpad: contains previous agent actions and tool outputs as a string.

Here’s an example:

from langchain_core.prompts import PromptTemplate

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)