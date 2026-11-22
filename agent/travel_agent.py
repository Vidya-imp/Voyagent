"""Builds the travel planning agent and runs it from the command line."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from agent.prompts import build_system_prompt
from tools.langchain_tools import ALL_TOOLS

load_dotenv()


def build_agent():
    """Create the tool-calling agent."""
    llm = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0)
    return create_agent(llm, ALL_TOOLS, system_prompt=build_system_prompt())


def plan_trip(query: str) -> str:
    """Run the agent on a user request and return the final text."""
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    question = ("Plan a 3-day, 2-night trip from Hyderabad to Delhi starting on "
                "2026-11-25. Budget 25000 rupees. I like temples and museums.")
    print(plan_trip(question))