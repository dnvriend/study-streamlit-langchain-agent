langchain-aws: 0.2.13
agents
Classes

agents.base.BedrockAgentAction

AgentAction with session id information.

agents.base.BedrockAgentFinish

AgentFinish with session id information.

agents.base.BedrockAgentsRunnable

Invoke a Bedrock Agent

agents.base.GuardrailConfiguration

Functions

agents.base.get_boto_session([...])

Construct the boto3 session

agents.base.parse_agent_response(response)

Parses the raw response from Bedrock Agent

chains
Functions

chains.graph_qa.neptune_cypher.create_neptune_opencypher_qa_chain(...)

Chain for question-answering against a Neptune graph by generating openCypher statements.

chains.graph_qa.neptune_cypher.extract_cypher(text)

Extract Cypher code from text using Regex.

chains.graph_qa.neptune_cypher.get_prompt(llm)

Selects the final prompt

chains.graph_qa.neptune_cypher.trim_query(query)

Trim the query to only include Cypher keywords.

chains.graph_qa.neptune_cypher.use_simple_prompt(llm)

Decides whether to use the simple prompt

chains.graph_qa.neptune_sparql.create_neptune_sparql_qa_chain(...)

Chain for question-answering against a Neptune graph by generating SPARQL statements.

chains.graph_qa.neptune_sparql.extract_sparql(query)

Extract SPARQL code from a text.

chains.graph_qa.neptune_sparql.get_prompt(...)

Selects the final prompt.

chat_models
Classes

chat_models.bedrock.ChatBedrock

A chat model that uses the Bedrock API.

chat_models.bedrock.ChatPromptAdapter()

Adapter class to prepare the inputs from Langchain to prompt format that Chat model expects.

chat_models.bedrock_converse.ChatBedrockConverse

Bedrock chat model integration built on the Bedrock converse API.

Functions

chat_models.bedrock.convert_messages_to_prompt_anthropic(...)

Format a list of messages into a full prompt for the Anthropic model

chat_models.bedrock.convert_messages_to_prompt_llama(...)

Convert a list of messages to a prompt for llama.

chat_models.bedrock.convert_messages_to_prompt_llama3(...)

Convert a list of messages to a prompt for llama.

chat_models.bedrock.convert_messages_to_prompt_mistral(...)

Convert a list of messages to a prompt for mistral.

document_compressors
Classes

document_compressors.rerank.BedrockRerank

Document compressor that uses AWS Bedrock Rerank API.

embeddings
Classes

embeddings.bedrock.BedrockEmbeddings

Bedrock embedding models.

function_calling
Classes

function_calling.AnthropicTool

function_calling.FunctionDescription

Representation of a callable function to send to an LLM.

function_calling.ToolDescription

Representation of a callable function to the OpenAI API.

function_calling.ToolsOutputParser

Functions

function_calling.convert_to_anthropic_tool(tool)

function_calling.get_system_message(tools)

graphs
Classes

graphs.neptune_graph.BaseNeptuneGraph()

graphs.neptune_graph.NeptuneAnalyticsGraph(...)

Neptune Analytics wrapper for graph operations.

graphs.neptune_graph.NeptuneGraph(host[, ...])

Neptune wrapper for graph operations.

graphs.neptune_graph.NeptuneQueryException(...)

Exception for the Neptune queries.

graphs.neptune_rdf_graph.NeptuneRdfGraph(host)

Neptune wrapper for RDF graph operations.

llms
Classes

llms.bedrock.AnthropicTool

llms.bedrock.BedrockBase

Base class for Bedrock models.

llms.bedrock.BedrockLLM

Bedrock models.

llms.bedrock.LLMInputOutputAdapter()

Adapter class to prepare the inputs from Langchain to a format that LLM model expects.

llms.sagemaker_endpoint.ContentHandlerBase()

A handler class to transform input from LLM to a format that SageMaker endpoint expects.

llms.sagemaker_endpoint.LLMContentHandler()

Content handler for LLM class.

llms.sagemaker_endpoint.LineIterator(stream)

A helper class for parsing the byte stream input.

llms.sagemaker_endpoint.SagemakerEndpoint

Sagemaker Inference Endpoint models.

Functions

llms.bedrock.extract_tool_calls(content)

llms.sagemaker_endpoint.enforce_stop_tokens(...)

Cut off the text as soon as any stop words occur.

retrievers
Classes

retrievers.bedrock.AmazonKnowledgeBasesRetriever

Amazon Bedrock Knowledge Bases retrieval.

retrievers.bedrock.RetrievalConfig

Configuration for retrieval.

retrievers.bedrock.SearchFilter

Filter configuration for retrieval.

retrievers.bedrock.VectorSearchConfig

Configuration for vector search.

retrievers.kendra.AdditionalResultAttribute

Additional result attribute.

retrievers.kendra.AdditionalResultAttributeValue

Value of an additional result attribute.

retrievers.kendra.AmazonKendraRetriever

Amazon Kendra Index retriever.

retrievers.kendra.DocumentAttribute

Document attribute.

retrievers.kendra.DocumentAttributeValue

Value of a document attribute.

retrievers.kendra.Highlight

Information that highlights the keywords in the excerpt.

retrievers.kendra.QueryResult

Amazon Kendra Query API search result.

retrievers.kendra.QueryResultItem

Query API result item.

retrievers.kendra.ResultItem

Base class of a result item.

retrievers.kendra.RetrieveResult

Amazon Kendra Retrieve API search result.

retrievers.kendra.RetrieveResultItem

Retrieve API result item.

retrievers.kendra.TextWithHighLights

Text with highlights.

Functions

retrievers.kendra.clean_excerpt(excerpt)

Clean an excerpt from Kendra.

retrievers.kendra.combined_text(item)

Combine a ResultItem title and excerpt into a single string.

utilities
Classes

utilities.redis.TokenEscaper([escape_chars_re])

Escape punctuation within an input string.

utilities.utils.DistanceStrategy(value)

Enumerator of the Distance strategies for calculating distances between vectors.

Functions

utilities.math.cosine_similarity(X, Y)

Row-wise cosine similarity between two equal-width matrices.

utilities.math.cosine_similarity_top_k(X, Y)

Row-wise cosine similarity with optional top-k and score threshold filtering.

utilities.redis.get_client(redis_url, **kwargs)

Get a redis client from the connection url given.

utilities.utils.filter_complex_metadata(...)

Filter out metadata types that are not supported for a vector store.

utilities.utils.maximal_marginal_relevance(...)

Calculate maximal marginal relevance.

utils
Functions

utils.anthropic_tokens_supported()

Check if all requirements for Anthropic count_tokens() are met.

utils.enforce_stop_tokens(text, stop)

Cut off the text as soon as any stop words occur.

utils.get_num_tokens_anthropic(text)

Get the number of tokens in a string of text.

utils.get_token_ids_anthropic(text)

Get the token ids for a string of text.

vectorstores
Classes

vectorstores.inmemorydb.base.InMemoryVectorStore(...)

InMemoryVectorStore vector database.

vectorstores.inmemorydb.base.InMemoryVectorStoreRetriever

Retriever for InMemoryVectorStore.

vectorstores.inmemorydb.cache.InMemorySemanticCache(...)

Cache that uses MemoryDB as a vector-store backend.

vectorstores.inmemorydb.filters.InMemoryDBFilter()

Collection of InMemoryDBFilterFields.

vectorstores.inmemorydb.filters.InMemoryDBFilterExpression([...])

Logical expression of InMemoryDBFilterFields.

vectorstores.inmemorydb.filters.InMemoryDBFilterField(field)

Base class for InMemoryDBFilterFields.

vectorstores.inmemorydb.filters.InMemoryDBFilterOperator(value)

InMemoryDBFilterOperator enumerator is used to create InMemoryDBFilterExpressions

vectorstores.inmemorydb.filters.InMemoryDBNum(field)

InMemoryDBFilterField representing a numeric field in a InMemoryDB index.

vectorstores.inmemorydb.filters.InMemoryDBTag(field)

InMemoryDBFilterField representing a tag in a InMemoryDB index.

vectorstores.inmemorydb.filters.InMemoryDBText(field)

InMemoryDBFilterField representing a text field in a InMemoryDB index.

vectorstores.inmemorydb.schema.FlatVectorField

Schema for flat vector fields in Redis.

vectorstores.inmemorydb.schema.HNSWVectorField

Schema for HNSW vector fields in Redis.

vectorstores.inmemorydb.schema.InMemoryDBDistanceMetric(value)

Distance metrics for Redis vector fields.

vectorstores.inmemorydb.schema.InMemoryDBField

Base class for Redis fields.

vectorstores.inmemorydb.schema.InMemoryDBModel

Schema for MemoryDB index.

vectorstores.inmemorydb.schema.InMemoryDBVectorField

Base class for Redis vector fields.

vectorstores.inmemorydb.schema.NumericFieldSchema

Schema for numeric fields in Redis.

vectorstores.inmemorydb.schema.TagFieldSchema

Schema for tag fields in Redis.

vectorstores.inmemorydb.schema.TextFieldSchema

Schema for text fields in Redis.

Functions

vectorstores.inmemorydb.base.check_index_exists(...)

Check if MemoryDB index exists.

vectorstores.inmemorydb.filters.check_operator_misuse(func)

Decorator to check for misuse of equality operators.

vectorstores.inmemorydb.schema.read_schema(...)

Read in the index schema from a dict or yaml file.