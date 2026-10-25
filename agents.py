from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage
from models import openai_model
from tools import search_web
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

#Creating sub-agents
logging.info("Creating sub-agent 1")
sub_agent1 = create_agent(model=openai_model, tools=[search_web], name="sub-agent-1")

logging.info("Creating sub-agent 2")
sub_agent2 = create_agent(model=openai_model, tools=[search_web], name="sub-agent-2")

@tool
def delegate_to_sub_agent1(query: str) -> str:
    """search the web for information on a given topic by delegating to sub-agent 1."""
    logging.info(f"Delegating to sub-agent 1 for query: {query}")
    response = sub_agent1.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][0].content
@tool
def delegate_to_sub_agent2(query: str) -> str:
    """search the web for information on a given topic by delegating to sub-agent 2."""
    logging.info(f"Delegating to sub-agent 2 for query: {query}")
    response = sub_agent2.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][0].content