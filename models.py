from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()
openai_model = init_chat_model("gpt-5-nano")