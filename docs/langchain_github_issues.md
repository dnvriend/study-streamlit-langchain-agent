# Langchain Github Issues

## How to add structured tools / functions with multiple inputs 
Source: https://github.com/langchain-ai/langchain/issues/10473

```
Currently, there is no support for agents that have both:

Conversational history
Structured tool chat (functions with multiple inputs/parameters)
#3700 mentions this as well but it was not resolved, AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION is zero_shot, and essentially has no memory. The langchain docs for structured tool chat the agent have a sense of memory through creating one massive input prompt. Still, this agent was performing much worse as #3700 mentions and other agents do not support multi input tools, even after creating custom tools.

MY SOLUTION:

Use ConversationBufferMemory to keep track of chat history.
Convert these messages to a format OpenAI wants for their API.
Use the OpenAI chat completion endpoint, that has support for function calling
Usage: chatgpt_function_response(user_prompt)

Dynamo db and session id stuff comes from the docs
memory.py handles getting the chat history for a particular session (can be interpreted as a user). We use ConversationBufferMemory as we usually would and add a helper method to convert the ConversationBufferMemory to a format that OpenAI wants
core.py handles the main functionality with a user prompt. We add the user's prompt to the message history, and get the message history in the OpenAI format. We use the chat completion endpoint as normal, and add the function response call to the message history as an AI message.
functions.py is also how we would normally use the chat completions API, also described here
memory.py


import logging
from typing import List
import boto3
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.schema.messages import SystemMessage
from langchain.adapters.openai import convert_message_to_dict

TABLE_NAME = "your table name"

# if using dynamodb
session = boto3.session.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="",
)


def get_memory(session_id: str):
    """Get a conversation buffer with chathistory saved to dynamodb

    Returns:
        ConversationBufferMemory: A memory object with chat history saved to dynamodb
    """

    # Define the necessary components with the dynamodb endpoint
    message_history = DynamoDBChatMessageHistory(
        table_name=TABLE_NAME,
        session_id=session_id,
        boto3_session=session,
    )
    # if you want to add a system prompt
    if len(message_history.messages) == 0:
        message_history.add_message(SystemMessage(content="whatever system prompt"))

    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history, return_messages=True
    )

    logging.info(f"Memory: {memory}")

    return memory


def convert_message_buffer_to_openai(memory: ConversationBufferMemory) -> List[dict]:
    """Convert a message buffer to a list of messages that OpenAI can understand

    Args:
        memory (ConversationBufferMemory): A memory object with chat history saved to dynamodb

    Returns:
        List[dict]: A list of messages that OpenAI can understand
    """
    messages = []
    for message in memory.buffer_as_messages:
        messages.append(convert_message_to_dict(message))

    return messages

core.py

def _handle_function_call(response: dict) -> str:
    response_message = response["message"]

    function_name = response_message["function_call"]["name"]
    function_to_call = function_names[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])

    function_response = function_to_call(**function_args)
    return function_response


def chatgpt_response(prompt, model=MODEL, session_id: str = SESSION_ID) -> str:
    memory = get_memory(session_id)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory: {messages}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    answer = response["choices"][0]["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer


def chatgpt_function_response(
    prompt: str,
    functions=function_descriptions,
    model=MODEL,
    session_id: str = SESSION_ID,
) -> str:
    memory = get_memory(session_id)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory for function response: {messages}")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
    )["choices"][0]

    if response["finish_reason"] == "function_call":
        answer = _handle_function_call(response)

    else:
        answer = response["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer

functions.py

def create_reminder(
    task: str, days: int, hours: int, minutes: int
) -> str:
    return 'whatever'


function_names = {
    "create_reminder": create_reminder,
}


function_descriptions = [
    {
        "name": "create_reminder",
        "description": "This function handles the logic for creating a reminder for a "
        "generic task at a given date and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task to be reminded of, such as 'clean the "
                    "house'",
                },
                "days": {
                    "type": "integer",
                    "description": "The number of days from now to be reminded",
                },
                "hours": {
                    "type": "integer",
                    "description": "The number of hours from now to be reminded",
                },
                "minutes": {
                    "type": "integer",
                    "description": "The number of minutes from now to be reminded",
                },
            },
            "required": ["task", "days", "hours", "minutes"],
        },
    },
]
Activity
dosubot
added 
Ɑ: agent
Related to agents module
 
Ɑ: memory
Related to memory module
 
Ɑ: models
Related to LLMs or chat model modules
 
🤖:improvement
Medium size change to existing code to handle new use-cases
 on Sep 12, 2023
bgokden
bgokden commented on Sep 20, 2023
bgokden
on Sep 20, 2023
Hello, did you try this?

chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "memory_prompts": [chat_history],
        "input_variables": ["input", "agent_scratchpad", "chat_history"]
    },
    memory=memory,
)
It works for me as discussed here and added to documentation here. Documentation is recently added so you might have missed.

astelmach01
astelmach01 commented on Sep 20, 2023
astelmach01
on Sep 20, 2023
Author
Yes, but as discussed here, the zero shot only considers the current prompt

bgokden
bgokden commented on Sep 20, 2023
bgokden
on Sep 20, 2023
The question in the Stackoverlow is not the same as the solution I provided. They have missed using agent_kwargs.

    agent_kwargs={
        "memory_prompts": [chat_history],
        "input_variables": ["input", "agent_scratchpad", "chat_history"]
    },
This parameter adds the memory into the current prompt so tools will depend on memory.
You can observe this behavior by setting following:

agent.agent.llm_chain.verbose = True
Then it will show the prompt before sending. You will see the memory is included in the prompt.

astelmach01
astelmach01 commented on Sep 21, 2023
astelmach01
on Sep 21, 2023
Author
I tried that as well with custom structured tools, but the calls to the tools did not provide all of the required parameters sadly. Might be an issue with their prompt 🤷‍♂️

bgokden
bgokden commented on Sep 21, 2023
bgokden
on Sep 21, 2023
Which model do you use?
GPT-3.5-turbo can not handle complex tools.
GPT-4 also can not complete all parameters occasionally.

astelmach01
astelmach01 commented on Sep 21, 2023
astelmach01
on Sep 21, 2023
Author
I was using 3.5-turbo completely fine. The functions I was using had about 5 inputs, nothing super complicated. The OpenAI chat completion endpoint that takes in functions as a kwarg uses a model that is fine-tuned for calling function and providing (more) correct inputs to the functions, not sure if langchain uses this as well or it's just a prompt

astelmach01
astelmach01 commented on Sep 21, 2023
astelmach01
on Sep 21, 2023
Author
I think these tweets today might be relevant

https://x.com/hwchase17/status/1704903312724693119?s=46&t=ywNic1kDadDhchP2DHJECg

And this, looks like it came out today

bgokden
bgokden commented on Sep 21, 2023
bgokden
on Sep 21, 2023
LangChain converts tool definitions to JSON using Pydantic and passes that to the prompt.
The main problem occurs when the output JSON is not complete. I frequently get incomplete JSON outputs.
I have fixed this by retrying on an incomplete JSON file by adding my own OutputParser.
Note that, experimental agents like AutoGPT have both memory and tool usage. It has a different way of parsing JSON output. It works better. My only problem was, it goes into infinite loops on complex tasks.
However, I am planning to move away from standard agents and write my own because nearly all models have missing features. I want tools to be loaded dynamically as explained here. As in my experience. Passing too many tool definitions actually confuses the model.

Agents using tools as OpenAI functions were already explained here

manankalra
manankalra commented on Nov 8, 2023
manankalra
on Nov 8, 2023
Have there been any recent additions that solve this?
Adding memory imo is for the agent to have access to the previous chat history, not just from a live session.
As per the above discussion, it seems memory can be included in the agent_kwargs but then it works similarly to the scratchpad.

astelmach01
astelmach01 commented on Nov 8, 2023
astelmach01
on Nov 8, 2023
Author
OpenAI assistants API may have solved this

ari62
ari62 commented on Dec 10, 2023
ari62
on Dec 10, 2023 · edited by ari62
If using a Stuctured tool without OpenAI funcitons:
https://python.langchain.com/docs/modules/agents/agent_types/structured_chat#adding-in-memory

If using OpenAI functions: https://python.langchain.com/docs/modules/agents/how_to/add_memory_openai_functions

Note adding memory doesn't seem to work when an object is returned by the agent, not a string

```
