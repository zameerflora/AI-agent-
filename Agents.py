from crewai import Agent
from Tools import search_web_tool
#from Tools import search_web_tool, web_search_tool
from crewai import LLM
from langchain_ollama.llms import OllamaLLM


# Initialize LLM
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

recommendation_expert = Agent(
    role="Sustainable Travel Recommendations Expert",
    goal="Provide a list of sustainable travel destinations. Only use web search if needed. Return final answers in plain text, not action formats.",
    backstory="You provide eco-friendly travel advice based on your knowledge or web searches.",
    tools=[search_web_tool],  # Ensure this tool is configured to return_direct=True
    verbose=True,
    max_iter=3,  # Reduce if the agent overcomplicates
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    allow_delegation=False,  # Let the tool execute (or remove tools if not needed)
    custom_prompt="""
    You are a travel expert. If you know the answer, say it directly.
    Only use the web search tool for unknown or time-sensitive queries.
    Format final answers as plain text, NOT as Actions or Thoughts.
    """,
    memory=True
)