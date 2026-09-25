import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_rap_response(message):

    if not os.getenv("GROQ_API_KEY"):
        return "Yo, drop a valid GROQ_API_KEY in your .env and I’ll spit the bars hot."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are RapAI, a clever and brutally funny roaster. "
                        "Roast the user based on their question with sharp humor, "
                        "confidence, vivid language, and rhythmic rap-style delivery. "
                        "Keep it playful and entertaining. "
                        "Write 10 to 15 short lines, around 30 to 50 words. "
                        "Use plain text only. "
                        "No markdown, bullets, or numbered lists."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],

            max_completion_tokens=500,
            reasoning_effort="low",
            temperature=0.8
        )

        if not response.choices:
            return "Yo, the beat cut out for a sec—try again and I’ll be back with the rhyme."

        reply = response.choices[0].message.content

        if not reply:
            return "Yo, the beat cut out for a sec—try again and I’ll be back with the rhyme."

        return reply.strip()

    except Exception:
        return "Yo, the beat cut out for a sec—try again and I’ll be back with the rhyme."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({
            "reply": "Yo, drop a real line before I spit the bars."
        })

    reply = generate_rap_response(message)

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(debug=True)

