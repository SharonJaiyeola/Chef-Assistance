# app.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "chefassistant"
CORS(app)

client = OpenAI(api_key="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")

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
