import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1. Define the Authority Whitelist
RELIABLE_DOMAINS = ["reuters.com", "bloomberg.com", "techcrunch.com", "bbc.com", "apnews.com"]

# 2. Define the Structured Response
class VerifiedNews(BaseModel):
    is_verified: bool = Field(description="True if news is found in reliable sources and cross-checked")
    headline: str = Field(description="The headline if verified, otherwise empty")
    summary: str = Field(description="The summary or 'No verified updates yet'")
    sources: list[str] = Field(description="List of URLs used for verification")

# 3. The Logic Engine
def get_verified_update(topic, search_results):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    prompt = ChatPromptTemplate.from_template("""
        You are a Fact-Checking Agent. Your goal is to verify news about {topic}.
        
        RULES:
        1. To be 'is_verified': True, the news MUST appear in at least 2 sources.
        2. AT LEAST ONE source must be from this list: {whitelist}.
        3. If these conditions are not met, set is_verified to False and summary to 'No verified updates yet'.
        
        DATA:
        {results}
    """)
    
    chain = prompt | llm | JsonOutputParser()
    
    return chain.invoke({
        "topic": topic,
        "whitelist": RELIABLE_DOMAINS,
        "results": search_results
    })