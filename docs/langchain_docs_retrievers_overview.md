# LangChain Docs Retrievers Overview
Source: https://python.langchain.com/docs/integrations/retrievers/

## Retrievers
A retriever is an interface that returns documents given an unstructured query. It is more general than a vector store. A retriever does not need to be able to store documents, only to return (or retrieve) them. Retrievers can be created from vector stores, but are also broad enough to include Wikipedia search and Amazon Kendra.

Retrievers accept a string query as input and return a list of Documents as output.

For specifics on how to use retrievers, see the relevant how-to guides here.

Note that all vector stores can be cast to retrievers. Refer to the vector store integration docs for available vector stores. This page lists custom retrievers, implemented via subclassing BaseRetriever.

Bring-your-own documents
The below retrievers allow you to index and search a custom corpus of documents.

Retriever	Self-host	Cloud offering	Package
AmazonKnowledgeBasesRetriever	❌	✅	langchain_aws
AzureAISearchRetriever	❌	✅	langchain_community
ElasticsearchRetriever	✅	✅	langchain_elasticsearch
MilvusCollectionHybridSearchRetriever	✅	❌	langchain_milvus
VertexAISearchRetriever	❌	✅	langchain_google_community
External index
The below retrievers will search over an external index (e.g., constructed from Internet data or similar).

Retriever	Source	Package
ArxivRetriever	Scholarly articles on arxiv.org	langchain_community
TavilySearchAPIRetriever	Internet search	langchain_community
WikipediaRetriever	Wikipedia articles	langchain_community
All retrievers
Name	Description
Activeloop Deep Memory	Activeloop Deep Memory is a suite of tools that enables you to optimi...
Amazon Kendra	Amazon Kendra is an intelligent search service provided by Amazon Web...
Arcee	Arcee helps with the development of the SLMs—small, specialized, secu...
Arxiv	arXiv is an open-access archive for 2 million scholarly articles in t...
AskNews	AskNews infuses any LLM with the latest global news (or historical ne...
Azure AI Search	Azure AI Search (formerly known as Azure Cognitive Search) is a Micro...
Bedrock (Knowledge Bases)	This guide will help you getting started with the AWS Knowledge Bases...
BM25	BM25 (Wikipedia) also known as the Okapi BM25, is a ranking function ...
Box	This will help you getting started with the Box retriever. For detail...
BREEBS (Open Knowledge)	BREEBS is an open collaborative knowledge platform.
Chaindesk	Chaindesk platform brings data from anywhere (Datsources: Text, PDF, ...
ChatGPT plugin	OpenAI plugins connect ChatGPT to third-party applications. These plu...
Cognee	This will help you getting started with the Cognee retriever. For det...
Cohere reranker	Cohere is a Canadian startup that provides natural language processin...
Cohere RAG	Cohere is a Canadian startup that provides natural language processin...
Dappier	Dappier connects any LLM or your Agentic AI to real-time, rights-clea...
DocArray	DocArray is a versatile, open-source tool for managing your multi-mod...
Dria	Dria is a hub of public RAG models for developers to both contribute ...
ElasticSearch BM25	Elasticsearch is a distributed, RESTful search and analytics engine. ...
Elasticsearch	Elasticsearch is a distributed, RESTful search and analytics engine. ...
Embedchain	Embedchain is a RAG framework to create data pipelines. It loads, ind...
FlashRank reranker	FlashRank is the Ultra-lite & Super-fast Python library to add re-ran...
Fleet AI Context	Fleet AI Context is a dataset of high-quality embeddings of the top 1...
Google Drive	This notebook covers how to retrieve documents from Google Drive.
Google Vertex AI Search	Google Vertex AI Search (formerly known as Enterprise Search on Gener...
Graph RAG	Graph traversal over any Vector Store using document metadata.
IBM watsonx.ai	WatsonxRerank is a wrapper for IBM watsonx.ai foundation models.
JaguarDB Vector Database	[JaguarDB Vector Database](http://www.jaguardb.com/windex.html
Kay.ai	Kai Data API built for RAG 🕵️ We are curating the world's largest da...
Kinetica Vectorstore based Retriever	Kinetica is a database with integrated support for vector similarity ...
kNN	In statistics, the k-nearest neighbours algorithm (k-NN) is a non-par...
LinkupSearchRetriever	Linkup provides an API to connect LLMs to the web and the Linkup Prem...
LLMLingua Document Compressor	LLMLingua utilizes a compact, well-trained language model (e.g., GPT2...
LOTR (Merger Retriever)	Lord of the Retrievers (LOTR), also known as MergerRetriever, takes a...
Metal	Metal is a managed service for ML Embeddings.
Milvus Hybrid Search	Milvus is an open-source vector database built to power embedding sim...
NanoPQ (Product Quantization)	Product Quantization algorithm (k-NN) in brief is a quantization algo...
needle	Needle Retriever
Nimble	NimbleSearchRetriever enables developers to build RAG applications an...
Outline	Outline is an open-source collaborative knowledge base platform desig...
Permit	Permit is an access control platform that provides fine-grained, real...
Pinecone Hybrid Search	Pinecone is a vector database with broad functionality.
PubMed	PubMed® by The National Center for Biotechnology Information, Nationa...
Qdrant Sparse Vector	Qdrant is an open-source, high-performance vector search engine/datab...
RAGatouille	RAGatouille makes it as simple as can be to use ColBERT!
RePhraseQuery	RePhraseQuery is a simple retriever that applies an LLM between the u...
Rememberizer	Rememberizer is a knowledge enhancement service for AI applications c...
SEC filing	SEC filing is a financial statement or other formal document submitte...
Self-querying retrievers	
SingleStoreDB	SingleStoreDB is a high-performance distributed SQL database that sup...
SVM	Support vector machines (SVMs) are a set of supervised learning metho...
TavilySearchAPI	Tavily's Search API is a search engine built specifically for AI agen...
TF-IDF	TF-IDF means term-frequency times inverse document-frequency.
**NeuralDB**	NeuralDB is a CPU-friendly and fine-tunable retrieval engine develope...
Vespa	Vespa is a fully featured search engine and vector database. It suppo...
Wikipedia	Overview
You.com	you.com API is a suite of tools designed to help developers ground th...
Zep Cloud	Retriever Example for Zep Cloud
Zep Open Source	Retriever Example for Zep
Zilliz Cloud Pipeline	Zilliz Cloud Pipelines transform your unstructured data to a searchab...