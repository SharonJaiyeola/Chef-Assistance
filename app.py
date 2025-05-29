# app.py
import os
from flask import Flask, request, jsonify, session
from flask import render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "chefassistant"
CORS(app)

# Use environment variable for API key (set this in Render dashboard)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if "chat_history" not in session:
        session["chat_history"] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful cooking assistant that only answers questions related to cooking, "
                    "African cuisine, or greetings. You do not respond to anything unrelated to these topics. "
                    "If a question is not about food, cooking techniques, ingredients, recipes, or greetings, respond with: "
                    "'I'm only here to help with cooking and African dishes. Please ask a food-related question.'"
                )
            }
        ]

    session["chat_history"].append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=session["chat_history"]
    )

    assistant_reply = response.choices[0].message.content
    session["chat_history"].append({"role": "assistant", "content": assistant_reply})

    return jsonify({"response": assistant_reply})


# This is required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)
