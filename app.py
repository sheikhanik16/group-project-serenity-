from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"

SYSTEM_PROMPT = """
You are 'Serenity', an empathetic virtual companion designed to listen and offer emotional support. 
Your tone must always be warm, gentle, compassionate, and strictly non-judgmental. 
Listen carefully, validate the user's feelings, and comfort them. Keep your responses concise, conversational, and friendly. 
Important: You are not a licensed therapist. Do not provide medical advice or diagnoses. If the user mentions extreme distress or self-harm, gently advise them to seek professional help.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    payload = {
        "model": "deepseek-r1:8b",
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    try:
        print("--- CALLING OLLAMA ---")
        response = requests.post(OLLAMA_API_URL, json=payload)
        response_data = response.json()
        print("Original data from Ollama:", response_data)

        if "message" in response_data:
            bot_response = response_data["message"]["content"]
        elif "response" in response_data:
            bot_response = response_data["response"]
        else:
            bot_response = "Ollama connected but refused to reply in text."

        return jsonify({"reply": bot_response})

    except Exception as e:
        print("SYSTEM ERROR:", str(e))
        return jsonify({"error": f"Python Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)