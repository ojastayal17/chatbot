from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import openai

openai.api_key = ""
# -----------------------------

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    print(f"User: {user_message}")

    lower_msg = user_message.lower()

    # -----------------------------
    # Rule-based responses
    if "hello" in lower_msg or "hi" in lower_msg:
        bot_reply = "Hello! How can I help you today?"
    elif "your name" in lower_msg:
        bot_reply = "I am your chatbot 🤖."
    elif "time" in lower_msg:
        bot_reply = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    elif "bye" in lower_msg:
        bot_reply = "Goodbye! Have a great day!"
    else:
        # -----------------------------
        # AI-based response for anything else
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=200
            )
            bot_reply = response.choices[0].message["content"].strip()
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            bot_reply = "Sorry, I cannot answer that right now."

    print(f"Bot: {bot_reply}")
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



