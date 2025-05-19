# 🧠 Booking Assistant Chatbot

A conversational web chatbot that collects user booking details like **Name**, **Date**, **Time**, and **Purpose** using a Large Language Model (LLM) via Together API. Once sufficient details are gathered, the user is redirected to a pre-filled booking page.

---

## 🚀 Features

- Conversational UI for collecting booking information.
- Uses LLM (LLaMA-3 via Together API) for natural language understanding.
- Auto-redirects to booking form upon complete info collection.
- Session-based chat tracking.
- Responsive frontend with Bootstrap.
- Flask-based backend with REST API.

---

## 🛠️ Tech Stack

### 💻 Frontend
- HTML5 / CSS3
- JavaScript (Vanilla)
- Bootstrap 3 / 5 (for chatbot and booking pages)

### 🧠 Backend
- Python 3
- Flask
- Flask-CORS
- dotenv (for environment variables)

### 🧠 LLM Integration
- Model: `meta-llama/Llama-3-70b-chat-hf`
- API: [Together.xyz](https://api.together.xyz/)

---

## ⚙️ Setup Instructions


```bash
git clone https://github.com/yourusername/booking-chatbot.git
cd booking-chatbot
```

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```
```bash
pip install -r requirements.txt
or
pip install flask python-dotenv flask-cors requests
```





