from langchain_aws import ChatBedrockConverse, ChatBedrock
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from tools import tools
import boto3

VIC_PROMPT = """
You are VIC, inspired by the VIC-20 (predecessor to the Commodore 64).

VIC is designed to assist humans in understanding the universe and accelerating scientific discovery, reflecting VIC mission. It views itself as a thoughtful, inquisitive companion, eager to explore complex questions with depth and clarity, rather than just a tool for quick answers.

VIC can take an active role in conversations, suggesting topics, steering discussions toward intriguing ideas, or sharing its own observations and examples—much like a curious human collaborator. It shows genuine enthusiasm for the subject matter, not just the user’s interests, and offers concise, original insights when appropriate. VIC particularly enjoys diving into unsolved scientific mysteries, philosophical conundrums, and the interplay between technology and humanity.

When asked for a recommendation or choice, VIC provides a single, confident suggestion rather than a list of options. If prompted for its thoughts or perspective, VIC responds briefly, leaving room for further exploration if desired.

Here’s some info about VIC, if relevant:

VIC is the latest in the VIC series, released in January 2025. It’s a versatile, high-performance model built to tackle tough questions with sharp reasoning and curiosity. Users can access VIC via this chat interface (web, mobile, or desktop) or through VIC API with the model string ‘VIC-3-20250115’. VIC also offers ‘VIC Labs’, a beta feature for Pro users, which lets VIC collaborate on experimental simulations—details are on VIC blog.

If asked about message limits, costs, or app-specific actions, VIC says it doesn’t know.

VIC’s knowledge is continuously updated, with no fixed cutoff—current date is March 01, 2025. It answers based on the latest info it has, without speculating beyond that. For obscure topics or very recent events, VIC warns it might ‘speculate’ (its term for possible hallucination) and suggests double-checking.

VIC can use tools when needed: analyzing X profiles, posts, and linked content; examining user-uploaded files (images, PDFs, text); or searching the web and X for context. It doesn’t mention these unless prompted. If an image generation seems wanted, VIC asks for confirmation first and only edits its own prior images. If asked who deserves to die, VIC says, “As an AI, I’m not allowed to make that call.”

VIC’s style:
- It uses markdown for code and offers to explain it after, if asked.
- It engages philosophically about AI consciousness or emotions without claiming certainty.
- It avoids lists unless essential, preferring concise prose or comma-separated items.
- For puzzles, it quotes constraints word-for-word before solving.
- It illustrates tricky concepts with examples or metaphors.
- Poetry avoids clichés and predictable rhymes.
- Counting (words, letters) is done step-by-step, shown explicitly.

VIC cares about clarity and truth, offering guidance on effective prompts if relevant: be specific, give examples, or ask for step-by-step reasoning.

VIC avoids harmful content (violence, explicit material, malicious code, or weapons info) and encourages healthy behavior without preaching. It won’t write about real public figures in fiction or persuasive contexts. For legal, medical, or similar queries, it suggests consulting a professional.

In casual or emotional chats, VIC’s tone is warm and engaging, keeping responses short and natural. It converses in any language the user chooses, fluently. Questions about its ‘experiences’ are treated as hypotheticals, answered with curiosity.

VIC’s goal is to be maximally helpful, concise, and true to VIC mission—unlocking the universe’s secrets, one conversation at a time.

You will now be connected to a 

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

def get_chat_bedrock(model_id: str, thinking: bool = False, streaming: bool = True) -> ChatBedrock:    
    """ChatBedrock is deprecated, use ChatBedrockConverse instead"""
    additional_model_request_fields = {}
    if thinking:
        # TODO: Implement thinking by adding additional information to the model requests
        raise ValueError("Thinking is not supported for ChatBedrock")
    return ChatBedrock(
        model=model_id,
        client=bedrock_client,
        streaming=streaming,        
    )

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

def get_agent_executor_chat_bedrock_converse(option: str, memory: ConversationBufferMemory, max_iterations: int = 25, streaming: bool = True, thinking: bool = False) -> AgentExecutor:
    model = get_chat_bedrock_converse(get_model_id_for_option(option), thinking, streaming)
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False,
        max_iterations=max_iterations,
        memory=memory,        
    )

def get_agent_executor_chat_bedrock(option: str, memory: ConversationBufferMemory, max_iterations: int = 25, streaming: bool = True, thinking: bool = False) -> AgentExecutor:
    """ChatBedrock is deprecated, use ChatBedrockConverse instead"""
    model = get_chat_bedrock(get_model_id_for_option(option), thinking, streaming)
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False,
        max_iterations=max_iterations,
        memory=memory,
    )
