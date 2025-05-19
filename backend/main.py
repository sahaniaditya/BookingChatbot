from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import requests
import os
import json
import re
from dotenv import load_dotenv
from flask_cors import CORS
from urllib.parse import urlencode

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains
app.secret_key = 'booking_app'

# Store user sessions
user_sessions = {}

#session handling
@app.route('/')
def home():
    username = session.get('username')
    return f'Welcome, {username}!' if username else 'You are not logged in.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Enter your name">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))

# Function to call LLM with current chat history
def call_llm(messages):
    response = requests.post(
        TOGETHER_API_URL,
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/Llama-3-70b-chat-hf",
            "messages": messages,
            "temperature": 0.7,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Utility to extract JSON fields from LLM output
def extract_json_from_text(text):
    try:
        json_part = re.search(r"{.*}", text, re.DOTALL).group(0)
        return json.loads(json_part)
    except Exception as e:
        print("Failed to extract JSON:", e)
        return {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    message = data.get("message")

    if not session_id or not message:
        return jsonify({"error": "Missing session_id or message"}), 400

    # Initialize session
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "chat": [{
                "role": "system",
                "content": (
                    "You are a helpful assistant collecting booking details. "
                    "Ask the user for their name, booking date, time, and purpose. "
                    "Once you have sufficient information, respond ONLY with a JSON like: "
                    '{ "name": "John", "date": "2025-05-18", "time": "2 PM", "purpose": "Meeting" }. '
                    "If you don’t have all fields yet, continue asking questions naturally."
                )
            }],
            "data": {}
        }

    # Add user message
    user_sessions[session_id]["chat"].append({"role": "user", "content": message})

    # Get model response
    bot_reply = call_llm(user_sessions[session_id]["chat"])

    # Add bot reply to session
    user_sessions[session_id]["chat"].append({"role": "assistant", "content": bot_reply})

    # Try to extract structured fields
    extracted = extract_json_from_text(bot_reply)
    user_sessions[session_id]["data"].update(extracted)
    current_data = user_sessions[session_id]["data"]

    # If all fields are available, generate redirect link
    required_fields = ["name", "date", "time", "purpose"]
    if all(field in current_data for field in required_fields):
        query_string = urlencode(current_data)
        redirect_url = f"file:///C:/Users/Dell/Desktop/project/frontend/booking.html?{query_string}"
        return jsonify({"reply": bot_reply, "redirect": redirect_url})
    else:
        return jsonify({"reply": bot_reply})
