from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

# Web search tool using DuckDuckGo
@tool
def search_web_tool(query: str)->str:
    """
    Searches the web for sustainable travel destinations and returns a CLEAN, SUMMARIZED answer.
    Use this only when you don't know the answer.
    """
    search_tool = DuckDuckGoSearchResults(num_results=5)

    results = search_tool.run(query)
    return f"Here are sustainable travel options based on web search:\n\n{results}"

# Web scraping tool
#web_search_tool = WebsiteSearchTool()
#scrape_website_tool = ScrapeWebsiteTool()