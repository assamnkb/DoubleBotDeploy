# Rasool Khan Real Estate — Chatbot Setup

## Project Structure
```
rasool_khan_realestate/
├── app.py              # Flask backend + Gemini AI
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Luxury UI frontend
└── README.md
```

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Gemini API Key

**Option A — Environment variable (recommended):**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

**Option B — Edit app.py directly:**
```python
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Get your free Gemini API key at: https://aistudio.google.com/app/apikey

### 3. Run the app
```bash
python app.py
```

Then open: http://localhost:5000

---

## Features
- 🤖 AI-powered by Gemini 2.0 Flash
- 💬 Conversational property consultation
- 📊 5 cities of dummy property data (Dubai, Karachi, Lahore, Islamabad, Riyadh)
- 🗂️ Live profile sidebar tracking user info
- 🏠 Property cards with pricing, amenities, and details
- 🌙 Luxury dark-gold aesthetic UI
- 📱 Mobile responsive

## How to get a Gemini API Key
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into the app

## Notes
- The AI uses `gemini-2.0-flash-exp` (Gemini 2.0 Flash Preview)
- All property data is dummy/simulated for demonstration
- Session data is stored in Flask server-side sessions
