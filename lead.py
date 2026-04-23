import json
lead_data = {}

def collect_lead_info(user_input):
    global lead_data

    # Step 1: Name
    if lead_data.get("step") == "name":
        lead_data["name"] = user_input   
        lead_data["step"] = "email"
        return "Got it! What's your email?"

    # Step 2: Email
    elif lead_data.get("step") == "email":
        if not user_input.endswith("@gmail.com"):
            return "Please enter a valid Gmail address (example@gmail.com)."
        lead_data["email"] = user_input
        lead_data["step"] = "platform"
        return "Great! Which platform do you create content on? (YouTube, Instagram, etc.)"

    # Step 3: Platform
    elif lead_data.get("step") == "platform":
        lead_data["platform"] = user_input
        return capture_lead()

    return "Something went wrong. Please try again."


def capture_lead():
    global lead_data

    clean_data = {
        "name": lead_data.get("name"),
        "email": lead_data.get("email"),
        "platform": lead_data.get("platform")
    }

    print(f"\nLead captured successfully: {clean_data}")

    # ✅ Append as JSON line (log style)
    with open("leads.json", "a") as f:
        f.write(json.dumps(clean_data) + "\n")

    lead_data = {}

    return "✅ Thanks! Our team will contact you soon."