def detect_intent(query):
    query = query.lower()

    # Greeting
    if query.strip() in ["hi", "hello", "hey"]:
        return "greeting"

    # Exit
    elif any(word in query for word in ["bye", "goodbye", "exit", "thanks", "thank you"]):
        return "exit"

    # BUY INTENT WITH PLAN
    elif ("buy" in query or "purchase" in query) and ("basic" in query or "pro" in query):
        return "lead"

    # General buy intent
    elif any(word in query for word in ["buy", "subscribe", "start", "try", "sign up"]):
        return "lead"

    # Product info
    elif any(word in query for word in [
        "price", "plan", "cost", "pricing", "product", "features",
        "refund", "policy", "support"
    ]):
        return "product"

    else:
        return "unknown"