from langchain_aws import ChatBedrock
import boto3
from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

model_arn = "arn:aws:bedrock:us-east-1:015242279314:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
max_tokens = 100000
temperature = 0

session = boto3.Session(region_name="us-east-1")
bedrock_client = session.client('bedrock-runtime', 'us-east-1')

# Create the base Claude model
claude_bedrock = ChatBedrock(
                  model_id=model_id,
                  provider="anthropic",
                  client=bedrock_client,
                  model_kwargs={
                      "temperature": temperature, 
                      "max_tokens": max_tokens,                      
                  },
                  streaming=True,
)

