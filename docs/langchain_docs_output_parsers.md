# Output parsers
Source: https://python.langchain.com/docs/concepts/output_parsers/

!!! IMPORTANT !!! 
!!!
We use ClaudeBedrock and Claude 3.5 or 3.7 and they both support tool calling and structured output parsing so this, an output parser, is not needed when we do tool calling.
!!!

> note: The information here refers to parsers that take a text output from a model try to parse it into a more structured representation. **More and more models are supporting function (or tool) calling, which handles this automatically. It is recommended to use function/tool calling rather than output parsing.** See documentation for that here.
!!! IMPORTANT !!! 

Output parser is responsible for taking the output of a model and transforming it to a more suitable format for downstream tasks. Useful when you are using LLMs to generate structured data, or to normalize output from chat models and LLMs.

LangChain has lots of different types of output parsers. This is a list of output parsers LangChain supports. The table below has various pieces of information:

Name: The name of the output parser
Supports Streaming: Whether the output parser supports streaming.
Has Format Instructions: Whether the output parser has format instructions. This is generally available except when (a) the desired schema is not specified in the prompt but rather in other parameters (like OpenAI function calling), or (b) when the OutputParser wraps another OutputParser.
Calls LLM: Whether this output parser itself calls an LLM. This is usually only done by output parsers that attempt to correct misformatted output.
Input Type: Expected input type. Most output parsers work on both strings and messages, but some (like OpenAI Functions) need a message with specific kwargs.
Output Type: The output type of the object returned by the parser.
Description: Our commentary on this output parser and when to use it.
Name	Supports Streaming	Has Format Instructions	Calls LLM	Input Type	Output Type	Description
Str	✅			str | Message	String	Parses texts from message objects. Useful for handling variable formats of message content (e.g., extracting text from content blocks).
JSON	✅	✅		str | Message	JSON object	Returns a JSON object as specified. You can specify a Pydantic model and it will return JSON for that model. Probably the most reliable output parser for getting structured data that does NOT use function calling.
XML	✅	✅		str | Message	dict	Returns a dictionary of tags. Use when XML output is needed. Use with models that are good at writing XML (like Anthropic's).
CSV	✅	✅		str | Message	List[str]	Returns a list of comma separated values.
OutputFixing			✅	str | Message		Wraps another output parser. If that output parser errors, then this will pass the error message and the bad output to an LLM and ask it to fix the output.
RetryWithError			✅	str | Message		Wraps another output parser. If that output parser errors, then this will pass the original inputs, the bad output, and the error message to an LLM and ask it to fix it. Compared to OutputFixingParser, this one also sends the original instructions.
Pydantic		✅		str | Message	pydantic.BaseModel	Takes a user defined Pydantic model and returns data in that format.
YAML		✅		str | Message	pydantic.BaseModel	Takes a user defined Pydantic model and returns data in that format. Uses YAML to encode it.
PandasDataFrame		✅		str | Message	dict	Useful for doing operations with pandas DataFrames.
Enum		✅		str | Message	Enum	Parses response into one of the provided enum values.
Datetime		✅		str | Message	datetime.datetime	Parses response into a datetime string.
Structured		✅		str | Message	Dict[str, str]	An output parser that returns structured information. It is less powerful than other output parsers since it only allows for fields to be strings. This can be useful when you are working with smaller LLMs.
For specifics on how to use output parsers, see the relevant how-to guides here.