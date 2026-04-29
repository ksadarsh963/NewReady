# NewReady: Event-Driven Automated News RAG System

**NewReady** is an intelligent news aggregation and verification pipeline designed for real-time, topic-specific updates. It leverages Retrieval-Augmented Generation (RAG) to ensure 100% data reliability by cross-referencing multiple sources before delivering insights.

## 🚀 Key Features
- **AI-Powered RAG:** Uses Groq (Llama 3.3) and sentence-transformers for high-speed, semantic news analysis.
- **Reliability Engine:** Automated integrity verification that cross-checks news across multiple reliable sources.
- **Event-Driven Automation:** Integrated with **n8n** and **Supabase** to trigger real-time Telegram alerts upon news verification.
- **CI/CD Integrated:** Automated testing via **GitHub Actions** to ensure execution readiness on every commit.
- **User-Centric:** Supports customizable update intervals and specific interest areas via a cloud-synced dashboard.

## 🛠️ Tech Stack
- **Languages:** Python (Backend), SQL (Supabase/PostgreSQL), Dart (Flutter Frontend)
- **AI/ML:** Groq API (Llama 3.3), LangChain, Hugging Face Embeddings
- **Infrastructure:** Supabase (Vector Store & Database), n8n (Workflow Automation)
- **DevOps:** GitHub Actions, Git

## 🏗️ System Architecture
1. **Search & Retrieval:** System identifies latest news via Tavily/Search APIs based on user-subscribed topics.
2. **Verification:** RAG chain verifies facts and checks source reliability using Llama 3.3.
3. **Storage:** Verified data is pushed to a Supabase PostgreSQL instance.
4. **Alerting:** An n8n webhook detects the new entry and pushes a formatted Markdown message to the user via Telegram Bot API.

## 📊 Database Logic (Example Query)
The system utilizes complex relational logic to manage user subscriptions. 
```sql
SELECT s.user_email, n.topic, n.content->>'headline' as headline
FROM user_subscriptions s
JOIN verified_news n ON s.topic = n.topic
WHERE s.user_email = 'user@example.com'
ORDER BY n.created_at DESC;
