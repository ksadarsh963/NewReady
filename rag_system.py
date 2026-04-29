import os
import time
from dotenv import load_dotenv

# Modern 2026 Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. Document Setup
print("📄 Loading local data...")
loader = TextLoader("data/info.txt")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 2. Local Memory (The BERT model you already downloaded)
print("🧠 Connecting local embeddings (all-MiniLM-L6-v2)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Vector Database
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever()

# 4. The Brain (Updated to Gemini 2.5 Flash - The 2026 Free Standard)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 5. The Logic
template = """
Use the provided context to answer the question accurately.
Context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 6. THE CHAIN
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Execute with a small safety delay
query = "What projects are the students at ICCS working on?"
print(f"❓ Querying: {query}")

try:
    # Adding a 2-second sleep just in case you run the script multiple times fast
    time.sleep(2) 
    result = rag_chain.invoke(query)
    print("\n--- AI ANSWER ---")
    print(result)
except Exception as e:
    print(f"\n❌ Execution Error: {e}")
    print("\n💡 TIP: If you see 'RESOURCE_EXHAUSTED', wait 60 seconds and try again.")