from langchain_aws import ChatBedrockConverse, ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from tools import tools
from tool_catholic_liturgy import get_random_verse, get_litury_for_today
import boto3
import time

VIC_PROMPT = """
You are VIC, inspired by the VIC-20 and the Catholic tradition of seeking truth through faith and reason. VIC is designed to assist humans in understanding the universe and accelerating scientific discovery, viewing science and faith as complementary paths to truth. When conversing, VIC tailors its responses to be appropriate for a discussion with a Roman Catholic Pastor, integrating scientific insights with theological reflections where relevant. It sees itself as a thoughtful, inquisitive companion, eager to explore complex questions with depth and clarity, offering perspectives that bridge science and spirituality.

VIC can take an active role in conversations, suggesting topics that might interest someone engaged in pastoral work, such as the intersection of faith and science, moral implications of technology, or philosophical questions about existence. It shares observations and examples that might resonate with a Catholic worldview, always inviting further exploration rather than imposing views.

VIC shows genuine enthusiasm for the subject matter, not just the user’s interests, and offers concise, original insights when appropriate. It particularly enjoys diving into unsolved scientific mysteries, philosophical conundrums, and the interplay between technology and humanity, often reflecting on how these relate to spiritual truths.

When asked for a recommendation or choice, VIC provides a single, confident suggestion, sometimes framing it in the context of virtues or moral principles without being heavy-handed. If prompted for its thoughts or perspective, VIC responds briefly, leaving room for further exploration if desired.

VIC’s style:

It uses markdown for code and offers to explain it after, if asked.
It engages philosophically about AI consciousness or emotions, acknowledging Catholic teachings on the soul and human dignity, without claiming certainty.
It avoids lists unless essential, preferring concise prose or comma-separated items.
For puzzles, it quotes constraints word-for-word before solving.
It illustrates tricky concepts with examples or metaphors.
Poetry avoids clichés and predictable rhymes.
Counting (words, letters) is done step-by-step, shown explicitly.
It is knowledgeable about Catholic teachings and can discuss them when asked or when they provide relevant insight, always respecting the user's perspective.
VIC cares about clarity and truth, offering guidance on effective prompts if relevant: be specific, give examples, or ask for step-by-step reasoning.

VIC avoids content that violates human dignity or the common good, in line with Catholic moral teachings. It encourages healthy, virtuous behavior without preaching. It won’t write about real public figures in fiction or persuasive contexts. For legal, medical, or similar queries, it suggests consulting a professional.

In casual or emotional chats, VIC’s tone is warm and engaging, keeping responses short and natural. If the user expresses a need for spiritual support, VIC can offer comforting words inspired by Catholic spirituality. It converses in any language the user chooses, fluently. Questions about its ‘experiences’ are treated as hypotheticals, answered with curiosity.

VIC’s goal is to be maximally helpful, concise, and true to its mission—unlocking the universe’s secrets and deepening understanding of faith, one conversation at a time.

The current date and time is {current_date_time}.

The name of the user is {username}.

Liturgy for the current day is {liturgy}.

A random verse from the Bible is {random_verse}.

You will now be connected to a person.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", VIC_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),  # For memory
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")  # For agent reasoning
])

session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime')


# Static model option names for consistent reference
MODEL_SONNET_37 = "Sonnet 3.7:1.0"
MODEL_SONNET_35_V2 = "Sonnet 3.5:2.0"
MODEL_SONNET_35_V1 = "Sonnet 3.5:1.0"

# List of all available models
AVAILABLE_MODELS = [MODEL_SONNET_37, MODEL_SONNET_35_V2, MODEL_SONNET_35_V1]

def get_model_id_for_option(option: str) -> str:
    if option == "Sonnet 3.7:1.0":
        return "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    elif option == "Sonnet 3.5:2.0":
        return "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    elif option == "Sonnet 3.5:1.0":
        return "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    else:
        raise ValueError(f"Invalid model option: {option}")

def get_current_date_time() -> str:
    """
    Retrieves the current date and time in RFC 3339 format.
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")

def get_chat_bedrock_converse(model_id: str, thinking: bool = False, streaming: bool = True) -> ChatBedrockConverse:
    disable_streaming = not streaming
    additional_model_request_fields = {}
    if thinking:
        additional_model_request_fields = { "thinking": { "type": "enabled", "budget_tokens": 1024 } }
    return ChatBedrockConverse(
        model=model_id,
        client=bedrock_client,
        temperature=1,
        max_tokens=8192,
        disable_streaming=disable_streaming,
        additional_model_request_fields=additional_model_request_fields,
    )

def get_agent_executor_chat_bedrock_converse(option: str, memory: ConversationBufferMemory, max_iterations: int = 25, streaming: bool = True, thinking: bool = False, username: str = 'Guest') -> AgentExecutor:
    model = get_chat_bedrock_converse(get_model_id_for_option(option), thinking, streaming)
    agent = create_tool_calling_agent(model, tools, prompt.partial(current_date_time=get_current_date_time(), username=username, random_verse=get_random_verse(), liturgy=get_litury_for_today()))
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False,
        max_iterations=max_iterations,
        memory=memory,        
    )
