from topic_agent.models import QueryUnderstanding
from topic_agent.llm.openai_client import OpenAIQueryUnderstandingClient


#made it rule based for now but will come back to change it to call an LLM API
def understand_query(query:str) -> QueryUnderstanding:
   client = OpenAIQueryUnderstandingClient()
   return client.understand_query(query)