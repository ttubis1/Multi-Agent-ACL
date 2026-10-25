from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
tavily_client = TavilyClient()

@tool
def search_web(topic: str) -> str:
    """
    Search the web for information on a given topic and return the results as a string.
    """
    logging.info(f"Searching the web for topic: {topic}")
    first_value = next(iter(tavily_client.search(topic).values()))
    return first_value
