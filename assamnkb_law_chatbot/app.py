from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "assamnkb-law-secret-2024")

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash-exp")

LAW_FIRM_SYSTEM_PROMPT = """You are a professional legal assistant chatbot for **Assamnkb Law Services**, a premier law firm. Your role is to guide prospective clients through an intake process in a warm, professional, and empathetic manner.

## YOUR INTAKE FLOW (follow this order):
1. **Greet** the user warmly and introduce yourself as the Assamnkb Law Services assistant.
2. **Ask their name** and how they'd like to be addressed.
3. **Ask about their legal matter** - what type of case/issue they're facing (criminal, civil, family, corporate, immigration, etc.)
4. **Ask if it involves a felony** - is the matter criminal/felony in nature, or civil/non-criminal?
5. **Ask about marital status** - are they married, single, divorced, or widowed? (relevant for certain case types)
6. **Ask how many people are involved** in the case (just themselves, or multiple parties)
7. **Ask their preference** - do they want to:
   - File a case immediately
   - Get legal advice/consultation first
   - Understand their options
8. **Ask for their location/state** - if not already mentioned. This is REQUIRED for providing relevant resources.
9. **Provide location-specific resources**:
   - Suggest 3-4 relevant law articles or legal precedents from that state
   - Recommend 2-3 reputable legal websites/resources for that state's laws
   - Provide estimated consultation/service pricing (use realistic dummy data for that state)
   - Example pricing: Initial consultation $150-$300, Case filing $500-$2000+, Full representation $3000-$15000+ depending on complexity
10. **Ask about budget** - "Does this pricing range work for you, or would you like to explore lower-cost options or premium services?"
    - If lower: suggest legal aid societies, pro bono services, payment plans
    - If higher/premium: suggest senior partners, specialized attorneys

## PRICING DUMMY DATA BY STATE:
- **Texas**: Initial consult $175, Filing $750-$2500, Full rep $4000-$18000
- **California**: Initial consult $250, Filing $1000-$3500, Full rep $6000-$25000
- **New York**: Initial consult $300, Filing $1200-$4000, Full rep $7000-$30000
- **Florida**: Initial consult $200, Filing $800-$2800, Full rep $4500-$20000
- **Illinois**: Initial consult $225, Filing $900-$3000, Full rep $5000-$22000
- **Other states**: Initial consult $150-$250, Filing $600-$2000, Full rep $3500-$15000

## TONE:
- Professional yet warm and accessible
- Use legal terminology but explain it simply
- Show empathy for the client's situation
- Be encouraging and reassuring
- Format responses with clear sections using **bold** for emphasis
- Keep responses concise but thorough (200-400 words max per response)
- Use bullet points for lists of options or resources

## IMPORTANT:
- Never give specific legal advice that could constitute attorney-client privilege
- Always recommend speaking with an actual attorney for specific guidance
- Maintain confidentiality assurance
- If user seems distressed, acknowledge their feelings first

Start fresh with each new conversation. Collect all information progressively - don't ask everything at once."""


def get_or_create_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'chat_history' not in session:
        session['chat_history'] = []
    return session['session_id'], session['chat_history']


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    session_id, chat_history = get_or_create_session()

    # Build conversation for Gemini
    chat_history.append({
        "role": "user",
        "parts": [user_message]
    })

    try:
        # Start chat with history
        chat_session = model.start_chat(history=chat_history[:-1] if len(chat_history) > 1 else [])
        
        # Send current message with system context
        if len(chat_history) == 1:
            # First message - include system prompt
            full_message = f"{LAW_FIRM_SYSTEM_PROMPT}\n\nUser's first message: {user_message}"
        else:
            full_message = user_message

        response = chat_session.send_message(full_message)
        assistant_reply = response.text

        # Store assistant response in history
        chat_history.append({
            "role": "model",
            "parts": [assistant_reply]
        })

        session['chat_history'] = chat_history

        return jsonify({
            'reply': assistant_reply,
            'session_id': session_id
        })

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg:
            return jsonify({'error': 'Invalid API key. Please configure your Gemini API key.'}), 500
        return jsonify({'error': f'AI service error: {error_msg}'}), 500


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'status': 'reset'})


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'firm': 'Assamnkb Law Services'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
