import json

# Load knowledge base
def load_knowledge():
    with open("knowledge_base.json", "r") as file:
        data = json.load(file)
    return data

# Simple retrieval (basic RAG)
def get_relevant_info(query):
    data = load_knowledge()
    query = query.lower()

    results = []

    # If user asks pricing → return ALL plans
    if any(word in query for word in ["price", "pricing", "cost", "plan", "product", "products"]):
        return data["plans"]

    # Search specific plan
    for plan in data["plans"]:
        if plan["name"].lower().split()[0] in query:
            return plan

    # Search policies
    if any(word in query for word in ["refund", "policy", "support"]):
        return data["policies"]

    return "No relevant info found"