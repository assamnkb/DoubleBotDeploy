# ⚖️ Assamnkb Law Services — AI Legal Chatbot

A premium Flask-based legal intake chatbot powered by Google Gemini 2.0 Flash.

---

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

### 3. Run the App
```bash
python app.py
```

Visit: http://localhost:5000

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API Key | ✅ Yes |
| `SECRET_KEY` | Flask session secret | Recommended |

---

## 💬 Chatbot Flow

The assistant guides users through:

1. **Personal Info** — Name and how to address them
2. **Case Type** — Criminal, civil, family, corporate, etc.
3. **Felony Check** — Criminal/felony vs civil matter
4. **Marital Status** — Relevant for family/estate cases
5. **Parties Involved** — Number of people in the case
6. **Service Type** — File case vs legal advice
7. **Location/State** — For state-specific resources
8. **Resources & Pricing** — Articles, websites, estimated costs
9. **Budget Check** — Premium, standard, or low-cost options

---

## 📁 Project Structure

```
assamnkb_law/
├── app.py              # Flask application + Gemini integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── templates/
│   └── index.html      # Premium UI (single-file, no build step)
└── README.md
```

---

## 🎨 UI Features

- Dark luxury legal aesthetic with gold accents
- Animated background with gradient orbs
- Progressive intake steps sidebar
- Real-time typing indicator
- Markdown rendering in chat bubbles
- Quick topic buttons
- Mobile responsive
- Auto-greeting on page load

---

## ⚠️ Legal Disclaimer

This chatbot is for intake and informational purposes only. It does not constitute legal advice or establish an attorney-client relationship.
