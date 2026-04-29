import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. The Search Tool (Gathers Reliable Data)
# Note: You'll need a TAVILY_API_KEY (Free tier available)
search_tool = TavilySearchResults(max_results=3, search_depth="advanced")

# 2. The Reliable News Logic
def get_live_reliable_news(topic):
    # Step A: Search for news
    print(f"🔍 Searching for verified news on: {topic}...")
    raw_data = search_tool.invoke({"query": f"latest verified news about {topic} 2026"})
    
    # Step B: Summarize with a "Skeptical" personality
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt = ChatPromptTemplate.from_template("""
        You are a fact-checker. Summarize the following news about {topic}.
        Only include facts supported by multiple sources. 
        Exclude rumors or social media speculation.
        
        Sources: {sources}
    """)
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic, "sources": raw_data})

# Test it
# news_update = get_live_reliable_news("Kochi Infopark AI Jobs")
# print(news_update)