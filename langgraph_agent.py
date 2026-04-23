from langgraph.graph import StateGraph
from typing import TypedDict

from intent import detect_intent
from rag import get_relevant_info
from lead import collect_lead_info

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"


# 🔹 STATE (memory across conversation)
class AgentState(TypedDict):
    user_input: str
    intent: str
    response: str
    lead_mode: bool


# 🔹 Step 1: Detect Intent
def intent_node(state: AgentState):
    if state.get("lead_mode"):
        return {**state, "intent": "lead"}

    intent = detect_intent(state["user_input"])
    return {**state, "intent": intent}


# 🔹 Step 2: Handle Greeting
def greeting_node(state: AgentState):
    return {**state, "response": "Hello! How can I help you today?"}


# 🔹 Step 3: Product + RAG
def product_node(state: AgentState):
    context = get_relevant_info(state["user_input"])

    prompt = f"""
You are a strict assistant for AutoStream SaaS.

ONLY answer using provided data.

Data:
{context}

User Question:
{state["user_input"]}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    answer = response.json()["choices"][0]["message"]["content"]

    return {**state, "response": answer}


# Step 4: Lead Handling
def lead_node(state: AgentState):
    user_input = state["user_input"].lower()

    # FIRST ENTRY
    if not state.get("lead_mode"):
        state["lead_mode"] = True

        from lead import lead_data
        lead_data.clear()
        lead_data["step"] = "name"

        #PLAN DETECTION
        if "basic" in user_input:
            state["selected_plan"] = "Basic"
            return {
                **state,
                "response": "Great choice! Basic Plan is $29/month.\nWhat's your name?"
            }

        elif "pro" in user_input:
            state["selected_plan"] = "Pro"
            return {
                **state,
                "response": "Awesome! Pro Plan is $79/month.\nWhat's your name?"
            }

        return {
            **state,
            "response": "Sure! Let's get you started. What's your name?"
        }

    # CONFIRM HANDLING
    if state.get("lead_mode") and state["user_input"] == "CONFIRM":
        return {
            **state,
            "response": "Perfect! Let's complete your details.\nWhat's your name?"
        }

    # CONTINUE FLOW
    result = collect_lead_info(state["user_input"])
    return {**state, "response": result}

def general_node(state: AgentState):
    prompt = f"""
You are a helpful SaaS assistant.

User:
{state["user_input"]}

Reply naturally.
"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    answer = response.json()["choices"][0]["message"]["content"]

    return {**state, "response": answer}

# ROUTER (brain of agent)
def router(state: AgentState):

    if state.get("lead_mode"):
        return "lead"

    if state["intent"] == "lead":
        return "lead"

    elif state["intent"] == "product":
        return "product"

    else:
        return "general" 


# 🔹 BUILD GRAPH
graph = StateGraph(AgentState)

graph.add_node("intent", intent_node)
graph.add_node("product", product_node)
graph.add_node("lead", lead_node)
graph.add_node("general", general_node)

graph.set_entry_point("intent")

graph.add_conditional_edges("intent", router)


graph.add_edge("product", "__end__")
graph.add_edge("lead", "__end__")
graph.add_edge("general", "__end__")

app = graph.compile()


# 🔹 MAIN LOOP
if __name__ == "__main__":
    print("🤖 AutoStream LangGraph Agent (type 'exit' to quit)\n")

    state = {
        "user_input": "",
        "intent": "",
        "response": "",
        "lead_mode": False
    }

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("AI: Goodbye! 👋")
            break

        state["user_input"] = user_input

        result = app.invoke(state)

        print("AI:", result["response"])

        state = result 

        # Stop lead mode after completion
        if result["response"] and "Thanks!" in result["response"]:
            state["lead_mode"] = False

