# A multiple function calling agent that can call multiple functions
Source: https://cobusgreyling.medium.com/openai-multi-functions-agent-4bf8c88c4b6e

TL;DR it can call multiple function but the caveat is that the function can only have a single argument.

# OpenAI Multi-Functions Agent
This article showcases how an autonomous agent can use the OpenAI function calling ability to respond to user prompts using a Large Language Model (LLM).
Cobus Greyling
Cobus Greyling

·
Follow

6 min read
·
Jun 27, 2023
33


1





I’m currently the Chief Evangelist @ HumanFirst. I explore & write about all things at the intersection of AI and language; ranging from LLMs, Chatbots, Voicebots, Development Frameworks, Data-Centric latent spaces & more.

In a previous article I discussed how OpenAI Function Calling can be used within an IDE like Flowise to create a high level of automation between a Prompt Chaining application and API Calls.

In the case of Prompt Chaining the chain of LLM prompts are design and sequenced as a state machine. With each node of the chain being connected.

Agents involve an LLM making decisions about which Actions to take, taking that Action, seeing an Observation, and repeating that until done.

LangChain provides a standard interface for agents, a selection of agents to choose from, and examples of end-to-end agents. — LangChain

As described in the previous quote, Agents have access to an array of tools at its disposal and leverages a LLM to make decisions as to which tool to use.

The agent continues to iterate until the final answer is reached. The level of autonomy of agents and their ability to perform chain-of-thought reasoning is what sets them apart.

The code example below not only illustrates how an Autonomous Agent goes about solving for a question.

The fully working example code below also shows how the agent uses OpenAI Function Calling within its own process to format and structure information exchanges between tools.

The code below can be copied into a notebook verbatim and run.

OpenAI, LangChain and Google Search need to be installed.

pip install langchain openai google-search-results
Import and make modules available:

from langchain import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
You will require an OpenAI and SerpAPI api key.

import os
import openai
os.environ['OPENAI_API_KEY'] = str("xxxxxxxxxxxxxxxx")
os.environ["SERPAPI_API_KEY"] = str("xxxxxxxxxxxxxxxx")
Below the OpenAI turbo model is defined and the tool defined with the name Search. The description is also defined here.

# Initialize the OpenAI language model
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual OpenAI key.
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Initialize the SerpAPIWrapper for search functionality
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual SerpAPI key.
search = SerpAPIWrapper()

# Define a list of tools offered by the agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful when you need to answer questions about current events. You should ask targeted questions."
    ),
]
Create verbose output from LangChain:

import langchain
langchain.debug = True
The agent is initialised:

mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True)
This is how you submit a question to the agent:

mrkl.run("What is the weather in LA and SF?")
Below is the complete response and process the Agent runs through to eventually reach the final answer:

The weather in Los Angeles is currently a few clouds with a low of around 60°F. The weather in San Francisco is currently partly cloudy with a low of 53°F.

[chain/start] 

[1:chain:AgentExecutor] Entering Chain run with input:
{
  "input": "What is the weather in LA and SF?"
}
[llm/start] [1:chain:AgentExecutor > 2:llm:ChatOpenAI] 
Entering LLM run with input:
{
  "prompts": [
    "System: You are a helpful AI assistant.\n
             Human: What is the weather in LA and SF?"
  ]
}
[llm/end] 

[1:chain:AgentExecutor > 2:llm:ChatOpenAI] [3.09s] 
Exiting LLM run with output:
{
  "generations": [
    [
      {
        "text": "",
        "generation_info": null,
        "message": {
          "content": "",
          "additional_kwargs": {
            "function_call": {
              "name": "tool_selection",
              "arguments": "{\n  \"actions\": [\n    {\n      \"action_name\": \"Search\",\n      \"action\": {\n        \"tool_input\": \"weather in Los Angeles\"\n      }\n    },\n    {\n      \"action_name\": \"Search\",\n      \"action\": {\n        \"tool_input\": \"weather in San Francisco\"\n      }\n    }\n  ]\n}"
            }
          },
          "example": false
        }
      }
    ]
  ],
  "llm_output": {
    "token_usage": {
      "prompt_tokens": 81,
      "completion_tokens": 75,
      "total_tokens": 156
    },
    "model_name": "gpt-3.5-turbo-0613"
  },
  "run": null
}
[tool/start] 
[1:chain:AgentExecutor > 3:tool:Search] Entering Tool run with input:
"{'tool_input': 'weather in Los Angeles'}"
[tool/end] 

[1:chain:AgentExecutor > 3:tool:Search] 
[419.339ms] 
Exiting Tool run with output:
"10 Day Weather-Los Angeles, CA. As of 2:59 am PDT. Tonight. --/60°. 2%. Mon 26 | Night. 60°. 2%. E 1 mph. A few clouds. Low around 60F."
[tool/start] [1:chain:AgentExecutor > 4:tool:Search] Entering Tool run with input:
"{'tool_input': 'weather in San Francisco'}"
[tool/end] [1:chain:AgentExecutor > 4:tool:Search] [286.71999999999997ms] Exiting Tool run with output:
"Partly cloudy skies during the evening will give way to cloudy skies overnight. Low 53F. Winds WSW at 10 to 20 mph. Humidity86%."
[llm/start] [1:chain:AgentExecutor > 5:llm:ChatOpenAI] Entering LLM run with input:
{
  "prompts": [
    "System: You are a helpful AI assistant.\nHuman: What is the weather in LA and SF?\nAI: {'name': 'tool_selection', 'arguments': '{\\n  \"actions\": [\\n    {\\n      \"action_name\": \"Search\",\\n      \"action\": {\\n        \"tool_input\": \"weather in Los Angeles\"\\n      }\\n    },\\n    {\\n      \"action_name\": \"Search\",\\n      \"action\": {\\n        \"tool_input\": \"weather in San Francisco\"\\n      }\\n    }\\n  ]\\n}'}\nFunction: 10 Day Weather-Los Angeles, CA. As of 2:59 am PDT. Tonight. --/60°. 2%. Mon 26 | Night. 60°. 2%. E 1 mph. A few clouds. Low around 60F.\nAI: {'name': 'tool_selection', 'arguments': '{\\n  \"actions\": [\\n    {\\n      \"action_name\": \"Search\",\\n      \"action\": {\\n        \"tool_input\": \"weather in Los Angeles\"\\n      }\\n    },\\n    {\\n      \"action_name\": \"Search\",\\n      \"action\": {\\n        \"tool_input\": \"weather in San Francisco\"\\n      }\\n    }\\n  ]\\n}'}\nFunction: Partly cloudy skies during the evening will give way to cloudy skies overnight. Low 53F. Winds WSW at 10 to 20 mph. Humidity86%."
  ]
}
WARNING:langchain.chat_models.openai:Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.<locals>._completion_with_retry in 1.0 seconds as it raised APIError: Bad gateway. {"error":{"code":502,"message":"Bad gateway.","param":null,"type":"cf_bad_gateway"}} 502 {'error': {'code': 502, 'message': 'Bad gateway.', 'param': None, 'type': 'cf_bad_gateway'}} {'Date': 'Tue, 27 Jun 2023 12:32:44 GMT', 'Content-Type': 'application/json', 'Content-Length': '84', 'Connection': 'keep-alive', 'X-Frame-Options': 'SAMEORIGIN', 'Referrer-Policy': 'same-origin', 'Cache-Control': 'private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0', 'Expires': 'Thu, 01 Jan 1970 00:00:01 GMT', 'Server': 'cloudflare', 'CF-RAY': '7dddaf4bcf411098-ORD', 'alt-svc': 'h3=":443"; ma=86400'}.
[llm/end] [1:chain:AgentExecutor > 5:llm:ChatOpenAI] [314.23s] Exiting LLM run with output:
{
  "generations": [
    [
      {
        "text": "The weather in Los Angeles is currently a few clouds with a low of around 60°F. The weather in San Francisco is currently partly cloudy with a low of 53°F.",
        "generation_info": null,
        "message": {
          "content": "The weather in Los Angeles is currently a few clouds with a low of around 60°F. The weather in San Francisco is currently partly cloudy with a low of 53°F.",
          "additional_kwargs": {},
          "example": false
        }
      }
    ]
  ],
  "llm_output": {
    "token_usage": {
      "prompt_tokens": 336,
      "completion_tokens": 37,
      "total_tokens": 373
    },
    "model_name": "gpt-3.5-turbo-0613"
  },
  "run": null
}
[chain/end] [1:chain:AgentExecutor] [318.03s] Exiting Chain run with output:
{
  "output": "The weather in Los Angeles is currently a few clouds with a low of around 60°F. The weather in San Francisco is currently partly cloudy with a low of 53°F."
}
The weather in Los Angeles is currently a few clouds with a low of around 60°F. The weather in San Francisco is currently partly cloudy with a low of 53°F.
Below is the JSON created by Function Calling:

{
 "actions": 
 [
  {
  "action_name": "Search",
   "action": 
   {
   "tool_input": "weather in Los Angeles"
   }
  },
  {
  "action_name": "Search",
   "action" : 
   {
   "tool_input": "weather in San Francisco"
   }
  }
 ]
}