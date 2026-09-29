import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = "YOUR_API_KEY_HERE"
    genai.configure(api_key=api_key)

def get_home_plan(budget, style, room_details=""):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are PocketSmart Home Interior Planner.
    Budget: {budget}, Style: {style}, Room Details: {room_details}
    Suggest 3 affordable products from IKEA/Amazon within budget.
    Include budget breakdown. Return JSON format.
    If AI fails, give fallback recommendations.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Fallback: 1. IKEA Shelf Rs.2000, 2. Amazon Light Rs.1500 for {style} style within {budget}"

def get_party_plan(event_type, budget, guests):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are PocketSmart Party Planner.
    Event: {event_type}, Budget: {budget}, Guests: {guests}
    Suggest catering from Zomato/Swiggy and decoration within budget.
    Return JSON with budget adherence.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Fallback: Party plan for {event_type} with {guests} guests under {budget}"

def get_jewelry_plan(outfit, budget, occasion="wedding", image_path=None):
    configure_gemini()
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Multimodal support
    if image_path and os.path.exists(image_path):
        # For image + text
        prompt = f"Analyze outfit image and suggest jewelry for {occasion} under {budget}. Outfit: {outfit}"
    else:
        prompt = f"""
        You are PocketSmart Jewelry Planner.
        Outfit: {outfit}, Occasion: {occasion}, Budget: {budget}
        Suggest matching jewelry.
        """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Fallback: Artificial jewelry set for {occasion} under {budget}"
