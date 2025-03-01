# LangChain Docs Tools Requests
Source: https://python.langchain.com/docs/integrations/tools/requests/

## Requests Toolkit
We can use the Requests toolkit to construct agents that generate HTTP requests.

For detailed documentation of all API toolkit features and configurations head to the API reference for RequestsToolkit.

## Setup
This toolkit lives in the langchain-community package:

```
%pip install -qU langchain-community
```

## Instantiation
First we will demonstrate a minimal example.

> Note: There are inherent risks in giving models discretion to execute real-world actions. We must "opt-in" to these risks by setting allow_dangerous_request=True to use these tools. This can be dangerous for calling unwanted requests. Please make sure your custom OpenAPI spec (yaml) is safe and that permissions associated with the tools are narrowly-scoped.

```python
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper

toolkit = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
)

tools = toolkit.get_tools()
```

## Available Tools

[RequestsGetTool(requests_wrapper=TextRequestsWrapper(headers={}, aiosession=None, auth=None, response_content_type='text', verify=True), allow_dangerous_requests=True),
 RequestsPostTool(requests_wrapper=TextRequestsWrapper(headers={}, aiosession=None, auth=None, response_content_type='text', verify=True), allow_dangerous_requests=True),
 RequestsPatchTool(requests_wrapper=TextRequestsWrapper(headers={}, aiosession=None, auth=None, response_content_type='text', verify=True), allow_dangerous_requests=True),
 RequestsPutTool(requests_wrapper=TextRequestsWrapper(headers={}, aiosession=None, auth=None, response_content_type='text', verify=True), allow_dangerous_requests=True),
 RequestsDeleteTool(requests_wrapper=TextRequestsWrapper(headers={}, aiosession=None, auth=None, response_content_type='text', verify=True), allow_dangerous_requests=True)]


- RequestsGetTool
- RequestsPostTool
- RequestsPatchTool
- RequestsPutTool
- RequestsDeleteTool

## Use within an agent

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(model="gpt-4o-mini")

system_message = """
You have access to an API to help answer user queries.
Here is documentation on the API:
{api_spec}
""".format(api_spec=api_spec)

agent_executor = create_react_agent(llm, tools, prompt=system_message)

example_query = "Fetch the top two posts. What are their titles?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
```
