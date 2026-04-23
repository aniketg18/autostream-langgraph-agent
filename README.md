# 🤖 AutoStream Conversational Agent (LangGraph)

This project is a conversational AI agent built using LangGraph that simulates a SaaS assistant for AutoStream. The agent can answer product-related queries, detect high-intent users, and capture leads through a structured conversation flow.

---

## 🚀 Features

- ✅ Natural conversation using LLM
- ✅ Intent detection (greeting, product, lead)
- ✅ RAG-based product & pricing responses
- ✅ High-intent detection (buy/subscribe)
- ✅ Lead collection (name, email, platform)
- ✅ Data persistence (stored in JSON log)

---

## 🧠 Tech Stack

- Python
- LangGraph
- OpenRouter API (LLaMA 3 8B)
- JSON (for knowledge base & storage)
- Any LLM (OpenAI, Claude, Gemini) can be integrated due to modular design

---

## 📁 Project Structure
autostream_agent/
│
├── langgraph_agent.py # Main agent logic (LangGraph flow)
├── intent.py # Intent detection logic
├── rag.py # RAG retrieval system
├── lead.py # Lead collection & storage
├── knowledge_base.json # Product & policy data
├── leads.json # Captured leads (log file)
├── requirements.txt
├── .gitignore
└── README.md

---

## ⚙️ How to Run Locally

### 1. Clone the repository
git clone https://github.com/your-username/autostream-langgraph-agent.git
cd autostream-langgraph-agent

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add API key
Create a `.env` file:  
OPENROUTER_API_KEY=your_api_key_here

### 5. Run the agent
python langgraph_agent.py

---

## 🧠 Architecture Explanation

This project uses LangGraph to design a structured conversational AI agent with clear control over execution flow. LangGraph was chosen because it allows defining modular nodes and conditional routing, unlike traditional LLM pipelines that are harder to control and debug.

The system is built as a graph with multiple nodes: intent detection, product retrieval (RAG), general conversation, and lead collection. The intent node classifies user input into categories such as greeting, product inquiry, or high-intent (buy). Based on this classification, the router directs the flow to the appropriate node.

State is managed using a shared dictionary (AgentState) that persists across user interactions. It stores user input, detected intent, response, and a lead_mode flag. When lead_mode is activated, the system bypasses intent detection and directly continues collecting user details step-by-step without breaking the flow.

For product-related queries, a simple RAG pipeline retrieves relevant information from a JSON knowledge base. The response is then generated using the LLaMA 3 8B model via OpenRouter API.

Lead data (name, email, platform) is collected sequentially and stored in a JSON file, simulating backend persistence. This modular and state-driven design makes the system scalable, maintainable, and closer to real-world applications.

---

## 📲 WhatsApp Deployment (Using Webhooks)

To deploy this agent on WhatsApp, we can use the WhatsApp Business API via Meta or Twilio.

### Approach:
1. Create a backend server using Flask or FastAPI.
2. Expose a webhook endpoint (e.g., `/webhook`).
3. WhatsApp sends incoming user messages to this webhook.
4. Extract the message and pass it to the LangGraph agent.
5. Process the response using the agent logic.
6. Send the reply back to the user via WhatsApp API.

This setup enables real-time communication and can be used for customer support, product queries, and automated lead generation.

---

## 🎥 Demo Video

The demo video demonstrates:

1. Agent answering pricing questions  
2. Detecting high-intent (buy intent)  
3. Collecting user details (name, email, platform)  
4. Successfully capturing leads  

👉 **Watch Demo Video Here:**  
[https://drive.google.com/file/d/19S3rC85o94j2T1MBfdr3gUNJ48LSlOYE/view?usp=sharing]

---

## 📌 Notes

- `.env` file is excluded for security reasons
- `leads.json` acts as a mock database for storing leads
- The system is CLI-based but designed for real-world deployment

---

## 👨‍💻 Author

Aniket Gaikwad
