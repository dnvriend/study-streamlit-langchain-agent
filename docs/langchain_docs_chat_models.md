Chat models
Chat models are language models that use a sequence of messages as inputs and return messages as outputs (as opposed to using plain text). These are generally newer models.

info
If you'd like to write your own chat model, see this how-to. If you'd like to contribute an integration, see Contributing integrations.

Select chat model:
pip install -qU "langchain[aws]"

# Ensure your AWS credentials are configured

from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic.claude-3-5-sonnet-20240620-v1:0", model_provider="bedrock_converse")

model.invoke("Hello, world!")

# Featured Providers

While all these LangChain classes support the indicated advanced feature, you may have to open the provider-specific documentation to learn which hosted models or backends support the feature.

Provider	Tool calling	Structured output	JSON mode	Local	Multimodal	Package
ChatAnthropic	✅	✅	❌	❌	✅	langchain-anthropic
ChatMistralAI	✅	✅	❌	❌	❌	langchain-mistralai
AzureChatOpenAI	✅	✅	✅	❌	✅	langchain-openai
ChatOpenAI	✅	✅	✅	❌	✅	langchain-openai
ChatVertexAI	✅	✅	❌	❌	✅	langchain-google-vertexai
ChatGoogleGenerativeAI	✅	✅	❌	❌	✅	langchain-google-genai
ChatGroq	✅	✅	✅	❌	❌	langchain-groq
ChatCohere	✅	✅	❌	❌	❌	langchain-cohere
ChatBedrock	✅	✅	❌	❌	❌	langchain-aws

