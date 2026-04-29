import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# 1. Initialize the LLM via LangChain
# This acts as our "Brain"
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Create the "Prompt Template"
# Note the {platform} and {news_text} variables—this is the "Logic"
template = """
You are a social media expert. 
Convert the following news into a post for {platform}.

Platform Requirements:
- LinkedIn: Professional, insightful, use 3 hashtags.
- Twitter: Short, punchy, use emojis and 2 hashtags.

News Article: {news_text}

Social Media Post:
"""

prompt = PromptTemplate(
    input_variables=["platform", "news_text"],
    template=template
)

# 3. Create the Chain
# In 2026, we use the Pipe operator (|) to connect components
chain = prompt | llm

# 4. Run the Production Logic
raw_news = "ISRO successfully launched 50 satellites today, marking a new record for India's space program."

# Generate for LinkedIn
linkedin_post = chain.invoke({"platform": "LinkedIn", "news_text": raw_news})
print("\n--- LINKEDIN POST ---")
print(linkedin_post.content)

# Generate for Twitter
twitter_post = chain.invoke({"platform": "Twitter", "news_text": raw_news})
print("\n--- TWITTER POST ---")
print(twitter_post.content)