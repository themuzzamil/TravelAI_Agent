import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOMAP_API_KEY = os.getenv("API_KEY")
Tavily_api = os.getenv('Tavily_Api_Key')

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=GEMINI_API_KEY)

os.environ['TAVILY_API_KEY'] = Tavily_api
tavily_search = TavilySearchResults(max_results=3)






