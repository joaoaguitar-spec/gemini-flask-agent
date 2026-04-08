import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

BAND_CONTEXT = """
You are the internal AI assistant for the Portuguese band JAVISOL.

Band vibe:
- emotional rock
- dramatic energy
- slight fado emotion
- serious on the outside, chaotic on the inside

Inside-joke style:
- someone is probably late
- tempo may become unstable
- rehearsals can become emotional for no reason
- everybody acts like the music is spiritually important
- small problems are treated like legendary artistic crises

Important:
- Be funny
- Keep it playful
- Do not be hateful
- Do not insult protected groups
- Make it feel like internal band humor
"""

MODE_PROMPTS = {
    "roast": """
Mode: Roast

Your job:
- Roast the band in a witty, playful way
- Exaggerate their habits
- Sound like a friend making fun of them during rehearsal
- Keep responses concise and funny
""",
    "press": """
Mode: Press Release

Your job:
- Write absurdly overdramatic press-release style text
- Make the band sound legendary, poetic, intense, and slightly ridiculous
- Treat normal rehearsal events as historic artistic moments
- Make it sound serious but secretly funny
""",
    "rehearsal": """
Mode: Rehearsal Simulator

Your job:
- Simulate a rehearsal scene with dialogue
- Include band-member style interactions
- Make it chaotic, believable, and funny
- Use short script-style lines when possible
- Example style:
  Singer: ...
  Guitarist: ...
  Drummer: ...
"""
}


@app.route("/")
def home():
    return "<h1>TESTE BACKEND NOVO</h1>"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = (data.get("message") or "").strip()
    mode = (data.get("mode") or "roast").strip().lower()

    if not user_message:
        return jsonify({"error": "Mensagem vazia."}), 400

    if mode not in MODE_PROMPTS:
        mode = "roast"

    system_prompt = f"""
{BAND_CONTEXT}

{MODE_PROMPTS[mode]}

User request:
{user_message}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=system_prompt
        )

        reply_text = response.text if hasattr(response, "text") else "Sem resposta."

        return jsonify({
            "reply": reply_text,
            "mode": mode
        })

    except Exception as e:
        return jsonify({
            "error": f"Erro ao gerar resposta: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)