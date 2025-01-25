from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Initialize the GenAI client
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY, http_options={"api_version": "v1alpha"})

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Extract user input
        data = request.json
        prompt = data.get("prompt", "")
        config = {"thinking_config": {"include_thoughts": True}}

        # Generate content using Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash-thinking-exp-01-21",
            contents=prompt,
            config=config
        )

        # Format the response
        output = {"response": [], "thoughts": []}
        for part in response.candidates[0].content.parts:
            if part.thought:
                output["thoughts"].append(part.text)
            else:
                output["response"].append(part.text)

        return jsonify(output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
