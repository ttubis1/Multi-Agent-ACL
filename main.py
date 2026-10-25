from prompts import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT
from langchain.agents import create_agent
from models import openai_model
from agents import delegate_to_sub_agent1, delegate_to_sub_agent2
import logging
from langchain.messages import SystemMessage, HumanMessage
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

#asking the user for their requirements
logging.info("Asking the user for their wedding requirements")
user_requirements = input("Please enter your wedding requirements: ")
#
#updating the system prompt with the user's requirements
updated_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=user_requirements)

#creating the main agent
logging.info("Creating the main agent")
main_agent = create_agent(
    model=openai_model,
    tools=[delegate_to_sub_agent1, delegate_to_sub_agent2],
    name="main-agent",
    system_prompt=updated_system_prompt)


#invoking the main agent with the user's prompt
logging.info("Invoking the main agent with the user's prompt")
response = main_agent.invoke({"messages": [HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]})

#printing the main agent's response
print("Main agent's response:")
print(response["messages"][-1].content)

