# LangChain How-To: Retrievers
Source: https://python.langchain.com/docs/how_to/agent_executor/

TL;DR: create a retriever, use from langchain.tools.retriever import create_retriever_tool to create a tool, add the tool to a list of tools, and pass the list of tools to an agent.

## What are Retrievers?

Retrievers are a core component in LangChain that provide a standardized interface for fetching relevant documents based on a query. Unlike vector stores which focus on **storage** and **similarity search**, retrievers are more general and flexible:

- They accept a string query as input and return a list of Documents as output
- They don't necessarily need to store documents themselves
- They can implement various retrieval strategies beyond vector similarity

As described in the [LangChain Retrievers documentation](https://python.langchain.com/docs/integrations/retrievers/), retrievers can be created from vector stores but also include broader search capabilities like Wikipedia.

## Types of Retrievers

LangChain offers a wide variety of retrievers:

1. **Bring-your-own-documents retrievers**:
   - AmazonKnowledgeBasesRetriever
   - AzureAISearchRetriever
   - ElasticsearchRetriever
   - And many others for custom document corpora

2. **External index retrievers**:
   - ArxivRetriever for scholarly articles
   - TavilySearchAPIRetriever for internet search
   - WikipediaRetriever for Wikipedia articles

3. **Specialized retrievers**:
   - Self-querying retrievers
   - Multi-query retrievers
   - Contextual compression retrievers
   - Ensemble retrievers (like LOTR/MergerRetriever)

## Retrievers in Agentic Architectures

In an agentic architecture, retrievers serve as knowledge-grounding tools that allow the agent to:

1. Access domain-specific knowledge not present in the LLM's training data
2. Retrieve up-to-date information from external sources
3. Search through private or proprietary documents
4. Ground responses in specific documentation or data sources

By integrating retrievers as tools, agents can dynamically decide when to retrieve information based on the task at hand, making them more versatile and accurate.

## Retrievers vs. RAG Pipelines

While retrievers are a component of RAG (Retrieval-Augmented Generation) pipelines, there are important distinctions in how they're used:

| Aspect | Retriever as Tool | RAG Pipeline |
|--------|------------------|--------------|
| Control | Agent decides when to use | Used automatically for every query |
| Integration | One of many tools | Central to the entire process |
| Flexibility | Can be bypassed when not needed | Always part of the workflow |
| Use case | Task-oriented, multi-step reasoning | Knowledge-intensive QA |

### When to Use RAG vs. Retriever Tools

**Use a RAG Pipeline When:**
- Questions are primarily factual and knowledge-based
- Consistency in knowledge access is critical
- The domain is narrow and well-defined
- You want to ensure every response is grounded in your documents

**Use a Retriever Tool When:**
- The agent needs to perform various tasks beyond just answering questions
- Knowledge retrieval is only occasionally needed
- The agent should decide when retrieval is necessary
- You want more control over when and how retrieval happens

## Integration with the Current Chatbot

Looking at the chatbot in `main.py`, adding retriever tools would be highly beneficial:

1. The current implementation already uses an `AgentExecutor` with various tools (math, shell, Python REPL)
2. The agent is powered by Claude 3.5 Sonnet, which can effectively reason about when to use different tools
3. Adding retriever tools would allow the chatbot to access domain-specific knowledge

For example, you could add:
- A retriever over your documentation to answer product questions
- A WikipediaRetriever for general knowledge
- A retriever over codebase documentation for development assistance

This would make the chatbot more knowledgeable while maintaining its ability to execute code and perform calculations.

## Implementation Strategy

To add retrievers to your agent:
1. Create the retriever (as shown in the code below)
2. Convert it to a tool using `create_retriever_tool`
3. Add it to your agent's tool list
4. The agent will automatically learn to use it when appropriate

## Crafting Effective Tool Descriptions

The description you provide for your retriever tool is crucial for guiding the agent on when and how to use it. A well-crafted tool description should:

1. Clearly state the tool's purpose
2. Specify the type of information it can retrieve
3. Provide guidance on when to use it
4. Include examples of good queries (optional)


# Retriever
We will also create a retriever over some data of our own. For a deeper explanation of each step here, see this tutorial.

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()

API Reference:WebBaseLoader | FAISS | OpenAIEmbeddings | RecursiveCharacterTextSplitter
retriever.invoke("how to upload a dataset")[0]
```

Now that we have populated our index that we will do doing retrieval over, we can easily turn it into a tool (the format needed for an agent to properly use it)

```python
from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

tools = [search, retriever_tool]
```

Tools
Now that we have created both, we can create a list of tools that we will use downstream.

# LangChain Reference: Retrievers, RAG, SQL Integration, and Custom Tools

## Introduction
This document serves as a reference for understanding how to integrate **retrievers, retrieval-augmented generation (RAG), SQL database support, and custom tools** into a LangChain-based agent. It also provides guidance on best practices for designing a system-level AI assistant capable of file operations, database interactions, and code execution.

---

## 1. Understanding Retrievers vs. RAG

### **Retrievers**
A **retriever** is a tool that fetches relevant documents or data in response to a query. Retrievers do not modify the data but return it as is. Examples include:

- **Wikipedia Retriever** – Retrieves topic-specific articles from Wikipedia.
- **SQL Query Retriever** – Fetches structured data from a database.
- **File Retriever** – Searches documents and retrieves relevant text sections.

### **Retrieval-Augmented Generation (RAG)**
- RAG combines a retriever with a generator (LLM) to improve responses.
- The retriever finds related text, and the LLM synthesizes an answer.
- **Downside:** RAG heavily depends on the quality of retrieved text. If the retriever returns partial, irrelevant, or out-of-context fragments, the LLM may generate inaccurate responses.
- **Typical issue with vector stores (e.g., FAISS):** Retrieved text fragments are sometimes **not directly relevant** because they are based on embedding similarity rather than direct document retrieval.

### **Key Takeaway for Beginners**
- Use **structured retrievers** (SQL queries, file search) for accurate, topic-specific responses.
- Use **RAG** when dealing with unstructured data that requires synthesis but ensure proper tuning of vector store parameters.

---

## 2. Adding SQL Database Support to a LangChain Agent

LangChain does not have a **dedicated SQL retriever** because SQL queries are structured and should be executed directly using SQLDatabaseChain.

### **Steps to Integrate SQL with an Agent**

#### **1. Install Dependencies**
```bash
pip install langchain langchain-experimental sqlalchemy boto3
```

#### **2. Set Up Database Connection**
```python
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import create_engine

database_uri = "postgresql+psycopg2://username:password@host:port/database_name"
engine = create_engine(database_uri)
db = SQLDatabaseChain(engine)
```

#### **3. Create SQLDatabaseChain**
```python
from langchain_experimental.sql import SQLDatabaseChain

sql_chain = SQLDatabaseChain.from_llm(llm=model, db=db, verbose=True)
```

#### **4. Convert SQL Chain into a Tool**
```python
from langchain_core.tools import Tool

sql_tool = Tool(
    name="sql_database",
    func=sql_chain.run,
    description="Query the SQL database for structured information."
)
```

#### **5. Add the Tool to the Agent**
```python
tools = [sql_tool]
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, memory=memory)
```

### **Why Use SQLDatabaseChain Instead of a Retriever?**
- SQL queries return structured, **direct answers** instead of vector-based approximations.
- **Retrievers** work well for **unstructured text**, while **SQL queries** are better for **structured data**.

---

## 3. Creating Custom Tools for AWS and System-Level Operations

If you need to add **AWS API capabilities** or **system-level operations** (file retrieval, shell commands, Python execution), you must create a **custom tool**.

### **Example: Creating an AWS S3 Bucket Listing Tool**
```python
from langchain_core.tools import tool
import boto3

@tool
def list_s3_buckets() -> str:
    """List all S3 buckets in your AWS account."""
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return f"Buckets: {', '.join(buckets)}"
```

### **Adding the Custom Tool to the Agent**
```python
tools = [list_s3_buckets]
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, memory=memory)
```

### **Security Considerations**
- Always use **IAM roles** and avoid hardcoding AWS credentials.
- Grant **least privilege access** to avoid security risks.

---

## 4. Choosing the Right Approach for Your Agent

### **When to Use a Retriever?**
- When fetching **pre-existing structured knowledge** (e.g., Wikipedia articles, file search, database queries via direct tools).
- When dealing with **structured responses** like retrieving a full document or a specific database entry.

### **When to Use RAG?**
- When the knowledge is **unstructured** and needs **synthesis** (e.g., answering open-ended questions based on document embeddings).
- When using **vector stores** (like FAISS) for semantic similarity search.

### **When to Use a Custom Tool?**
- When integrating with **external APIs** (AWS, databases, system commands).
- When enabling **operational capabilities** (e.g., executing Python code, running shell commands, modifying files).

### **Recommended Approach for System-Level Agents**
Given that you want to integrate **retrievers (file/database), database chains, shell tools, Python REPL, and system-level operations**, the best strategy is:
1. **Use structured retrievers** for direct document retrieval.
2. **Use SQLDatabaseChain** for structured data queries.
3. **Use custom tools** for AWS interactions, shell execution, and system tasks.
4. **Avoid pure RAG** unless you need synthesis from unstructured text.

---

## Conclusion
- **Retrievers provide direct, topic-specific information.**
- **RAG is useful for unstructured data but needs tuning.**
- **SQLDatabaseChain is the best way to interact with structured databases.**
- **Custom tools allow external API and system interactions.**
- **A hybrid approach combining retrievers, SQL chains, and tools is best for building a system-level AI assistant.**

This guide serves as a **quick reference** for beginners aiming to build an **effective LangChain-powered agent** with structured data retrieval, system operations, and external integrations.

