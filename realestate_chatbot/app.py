from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "rasool-khan-secret-2024")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

DUMMY_PROPERTIES = {
    "dubai": [
        {"name": "Palm Residences Tower A", "type": "apartment", "community": True, "bedrooms": 2, "price": 2800000, "area": "1450 sqft", "amenities": ["Pool", "Gym", "Concierge", "Beach Access"], "image_emoji": "🏙️"},
        {"name": "Al Barsha Villa Complex", "type": "villa", "community": True, "bedrooms": 4, "price": 5500000, "area": "3200 sqft", "amenities": ["Private Pool", "Garden", "Garage", "Security"], "image_emoji": "🏡"},
        {"name": "Downtown Loft Studio", "type": "studio", "community": False, "bedrooms": 1, "price": 900000, "area": "650 sqft", "amenities": ["Gym", "Rooftop", "Smart Home"], "image_emoji": "🌆"},
        {"name": "Jumeirah Golf Estates", "type": "villa", "community": True, "bedrooms": 5, "price": 8200000, "area": "5100 sqft", "amenities": ["Golf Course", "Pool", "Tennis", "Club House"], "image_emoji": "⛳"},
        {"name": "Marina Heights Penthouse", "type": "penthouse", "community": False, "bedrooms": 3, "price": 6700000, "area": "2800 sqft", "amenities": ["Sea View", "Private Terrace", "Butler Service"], "image_emoji": "🌊"},
    ],
    "karachi": [
        {"name": "DHA Phase 6 Bungalow", "type": "house", "community": False, "bedrooms": 4, "price": 45000000, "area": "400 sqyd", "amenities": ["Garden", "Garage", "Servant Quarters"], "image_emoji": "🏠"},
        {"name": "Emaar Creek Residences", "type": "apartment", "community": True, "bedrooms": 3, "price": 28000000, "area": "1800 sqft", "amenities": ["Sea View", "Pool", "Gym", "Security"], "image_emoji": "🌃"},
        {"name": "Clifton Block 2 Flat", "type": "apartment", "community": False, "bedrooms": 2, "price": 15000000, "area": "1100 sqft", "amenities": ["Generator", "Water Tank", "Parking"], "image_emoji": "🏢"},
        {"name": "Bahria Town Karachi Villa", "type": "villa", "community": True, "bedrooms": 5, "price": 65000000, "area": "500 sqyd", "amenities": ["Gated Community", "Park", "Mosque", "Mall Access"], "image_emoji": "🏘️"},
        {"name": "Gulshan-e-Iqbal House", "type": "house", "community": False, "bedrooms": 3, "price": 22000000, "area": "240 sqyd", "amenities": ["Rooftop", "Parking", "Gas"], "image_emoji": "🏡"},
    ],
    "lahore": [
        {"name": "DHA Phase 7 House", "type": "house", "community": False, "bedrooms": 5, "price": 55000000, "area": "1 Kanal", "amenities": ["Basement", "Garden", "3 Car Garage"], "image_emoji": "🏠"},
        {"name": "Bahria Orchard Villa", "type": "villa", "community": True, "bedrooms": 4, "price": 38000000, "area": "10 Marla", "amenities": ["Community Club", "Parks", "Security 24/7"], "image_emoji": "🌿"},
        {"name": "Gulberg Apartment", "type": "apartment", "community": False, "bedrooms": 2, "price": 18000000, "area": "1200 sqft", "amenities": ["Lift", "Generator", "Parking"], "image_emoji": "🏙️"},
        {"name": "Lake City Mansion", "type": "mansion", "community": True, "bedrooms": 6, "price": 120000000, "area": "2 Kanal", "amenities": ["Lake View", "Pool", "Home Theatre", "Smart Home"], "image_emoji": "🏰"},
        {"name": "Model Town House", "type": "house", "community": False, "bedrooms": 3, "price": 28000000, "area": "5 Marla", "amenities": ["Corner Plot", "Rooftop", "Garden"], "image_emoji": "🏡"},
    ],
    "islamabad": [
        {"name": "F-7 Sector House", "type": "house", "community": False, "bedrooms": 4, "price": 95000000, "area": "1 Kanal", "amenities": ["Basement", "Garden", "Servant Quarters", "Garage"], "image_emoji": "🌄"},
        {"name": "Park Enclave Villa", "type": "villa", "community": True, "bedrooms": 5, "price": 150000000, "area": "1 Kanal", "amenities": ["Margalla Hills View", "Gated", "Park", "School"], "image_emoji": "⛰️"},
        {"name": "Centaurus Apartment", "type": "apartment", "community": True, "bedrooms": 3, "price": 45000000, "area": "2100 sqft", "amenities": ["Mall Access", "Pool", "Gym", "Concierge"], "image_emoji": "🏙️"},
        {"name": "DHA Valley Plot House", "type": "house", "community": True, "bedrooms": 4, "price": 35000000, "area": "8 Marla", "amenities": ["Community", "Parks", "Sports Complex"], "image_emoji": "🏘️"},
        {"name": "E-11 Luxury Flat", "type": "apartment", "community": False, "bedrooms": 2, "price": 22000000, "area": "1400 sqft", "amenities": ["View", "Generator", "Parking", "Security"], "image_emoji": "🌃"},
    ],
    "riyadh": [
        {"name": "Al Olaya Tower Apartment", "type": "apartment", "community": True, "bedrooms": 3, "price": 1800000, "area": "1900 sqft", "amenities": ["Pool", "Gym", "Concierge", "Parking"], "image_emoji": "🏙️"},
        {"name": "Diplomatic Quarter Villa", "type": "villa", "community": True, "bedrooms": 5, "price": 4500000, "area": "550 sqm", "amenities": ["Private Pool", "Garden", "Maid Room", "Security"], "image_emoji": "🏡"},
        {"name": "Al Nakheel Compound", "type": "villa", "community": True, "bedrooms": 4, "price": 2900000, "area": "420 sqm", "amenities": ["Gated Community", "School", "Supermarket", "Clinic"], "image_emoji": "🌴"},
        {"name": "King Abdullah Road Flat", "type": "apartment", "community": False, "bedrooms": 2, "price": 950000, "area": "1100 sqft", "amenities": ["Balcony", "Storage", "Covered Parking"], "image_emoji": "🌆"},
        {"name": "Hittin District Mansion", "type": "mansion", "community": False, "bedrooms": 7, "price": 9800000, "area": "900 sqm", "amenities": ["Pool", "Home Cinema", "Smart Systems", "Majlis"], "image_emoji": "🏰"},
    ],
    "default": [
        {"name": "City Centre Apartment", "type": "apartment", "community": True, "bedrooms": 2, "price": 1500000, "area": "1100 sqft", "amenities": ["Pool", "Gym", "Parking"], "image_emoji": "🏢"},
        {"name": "Suburban Family Villa", "type": "villa", "community": True, "bedrooms": 4, "price": 3200000, "area": "2800 sqft", "amenities": ["Garden", "Pool", "Security", "School Nearby"], "image_emoji": "🏡"},
        {"name": "Compact Studio", "type": "studio", "community": False, "bedrooms": 1, "price": 450000, "area": "550 sqft", "amenities": ["Gym", "Security", "Transport Links"], "image_emoji": "🌆"},
        {"name": "Heritage Townhouse", "type": "townhouse", "community": True, "bedrooms": 3, "price": 2100000, "area": "1800 sqft", "amenities": ["Terrace", "Shared Garden", "Parking"], "image_emoji": "🏘️"},
        {"name": "Penthouse Suite", "type": "penthouse", "community": False, "bedrooms": 3, "price": 5500000, "area": "3000 sqft", "amenities": ["360° View", "Private Roof", "Smart Home"], "image_emoji": "✨"},
    ]
}

SYSTEM_PROMPT = """You are Riya, a warm, professional real estate assistant for "Rasool Khan Real Estate Services" — a premium real estate agency. Your personality is helpful, friendly, and knowledgeable.

Your goal is to gather information from the user in a natural conversational flow and ultimately suggest suitable properties. Collect these details one by one (don't ask everything at once):

1. **Occupation/Work** — what does the user do for a living?
2. **Marital Status** — married, single, or other?
3. **Household Size** — how many people will be living in the property?
4. **Property Preference** — do they prefer a standalone/independent house or a community-based living (gated community, apartment complex, etc.)?
5. **Location** — if not mentioned, ask for preferred city or area.

Once you have these details, analyze the dummy property data provided and suggest 3 suitable properties. For each suggestion explain WHY it's a good match based on their profile. After suggesting, ask if their budget is comfortable with these properties or if they'd like to explore cheaper or more premium options.

You have access to property data in JSON format which will be passed in context. Use it to make specific recommendations with property names and prices.

Keep responses concise (2-4 sentences max per message unless listing properties). Be warm and personable. Never list all questions at once — have a real conversation. 

When you have all information needed, output properties in this EXACT format at the end of your message:
[PROPERTIES_DATA: {"properties": [list of property names to show]}]

Currency formatting guide: 
- If price is in SAR/AED (Dubai/Riyadh) show as "AED X,XXX,XXX" or "SAR X,XXX,XXX"
- If price is in PKR (Karachi/Lahore/Islamabad) show as "PKR XX,XXX,XXX"
- Otherwise show with appropriate currency

Remember: You represent a premium brand. Always be respectful and professional."""

def get_properties_for_location(location: str) -> list:
    location_lower = location.lower()
    for city in DUMMY_PROPERTIES:
        if city in location_lower or location_lower in city:
            return DUMMY_PROPERTIES[city]
    return DUMMY_PROPERTIES["default"]

def chat_with_gemini(messages: list, user_profile: dict) -> str:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            system_instruction=SYSTEM_PROMPT
        )
        
        location = user_profile.get("location", "")
        properties = get_properties_for_location(location) if location else []
        
        context_message = ""
        if properties:
            context_message = f"\n\n[SYSTEM CONTEXT - Available properties in {location}]: {json.dumps(properties, indent=2)}"
        
        history = []
        for msg in messages[:-1]:
            history.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })
        
        chat = model.start_chat(history=history)
        
        last_user_msg = messages[-1]["content"]
        if context_message:
            last_user_msg += context_message
        
        response = chat.send_message(last_user_msg)
        return response.text
    except Exception as e:
        return f"I apologize, I'm having a brief technical issue. Please try again in a moment. (Error: {str(e)})"

@app.route("/")
def index():
    session["session_id"] = str(uuid.uuid4())
    session["messages"] = []
    session["user_profile"] = {}
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    if "messages" not in session:
        session["messages"] = []
    if "user_profile" not in session:
        session["user_profile"] = {}
    
    messages = session["messages"]
    user_profile = session["user_profile"]
    
    # Update location if detected
    location_keywords = ["dubai", "karachi", "lahore", "islamabad", "riyadh", "in ", "at ", "near "]
    for keyword in ["dubai", "karachi", "lahore", "islamabad", "riyadh"]:
        if keyword in user_message.lower():
            user_profile["location"] = keyword
            session["user_profile"] = user_profile
            break
    
    if not messages:
        messages.append({
            "role": "user",
            "content": "Hello, I'm looking for a property."
        })
        messages.append({
            "role": "model",
            "content": "Hello! Welcome to Rasool Khan Real Estate Services! 🏠 I'm Riya, your personal property consultant. I'm thrilled to help you find your perfect home!\n\nTo get started — could you tell me a little about yourself? What do you do for work?"
        })
    
    messages.append({"role": "user", "content": user_message})
    
    ai_response = chat_with_gemini(messages, user_profile)
    
    messages.append({"role": "model", "content": ai_response})
    session["messages"] = messages
    
    # Extract properties data if present
    properties_data = None
    clean_response = ai_response
    if "[PROPERTIES_DATA:" in ai_response:
        try:
            start = ai_response.index("[PROPERTIES_DATA:") + len("[PROPERTIES_DATA:")
            end = ai_response.index("]", start)
            json_str = ai_response[start:end]
            properties_json = json.loads(json_str)
            property_names = properties_json.get("properties", [])
            
            location = user_profile.get("location", "")
            all_props = get_properties_for_location(location) if location else get_properties_for_location("")
            
            properties_data = [p for p in all_props if p["name"] in property_names]
            if not properties_data:
                properties_data = all_props[:3]
            
            clean_response = ai_response[:ai_response.index("[PROPERTIES_DATA:")].strip()
        except:
            pass
    
    return jsonify({
        "response": clean_response,
        "properties": properties_data
    })

@app.route("/reset", methods=["POST"])
def reset():
    session["messages"] = []
    session["user_profile"] = {}
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
