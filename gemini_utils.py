import google.generativeai as genai
import os

# Gemini setup - API key will be loaded from environment
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    genai.configure(api_key=api_key)

def get_home_plan(budget, style):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are PocketSmart Home Planner.
    User Budget: {budget}
    Style: {style}
    Suggest 3 affordable home interior items within budget with store names.
    Return in JSON format.
    """
    response = model.generate_content(prompt)
    return response.text

def get_party_plan(event_type, budget, guests):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are PocketSmart Party Planner.
    Event: {event_type}, Budget: {budget}, Guests: {guests}
    Suggest catering and decoration plan.
    Return in JSON format.
    """
    response = model.generate_content(prompt)
    return response.text

def get_jewelry_plan(outfit, budget):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are PocketSmart Jewelry Planner.
    Outfit: {outfit}, Budget: {budget}
    Suggest matching jewelry that fits budget.
    Return in JSON format.
    """
    response = model.generate_content(prompt)
    return response.text
