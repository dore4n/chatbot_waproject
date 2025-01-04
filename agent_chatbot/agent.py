import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun(backend='auto')

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

message_history = [] 
user_preferences = {}  


llm_generic = ChatGroq(
    model="llama-3.2-90b-vision-preview",
    temperature=0,
    max_tokens=500,
    timeout=None,
    max_retries=2
)

research_agent = create_react_agent(
    llm_generic,
    tools=[DuckDuckGoSearchRun()],
    state_modifier="""
        Você é especializado em realizar pesquisas detalhadas sobre um tema...
    """
)
