import os
from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

# Get the API key from the environment
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("The GENAI_API_KEY environment variable is not set. Please set it in your environment or .env file.")

# Initialize the Flask app
app = Flask(__name__)

# Initialize the GenAI client
client = genai.Client(api_key=GENAI_API_KEY, http_options={"api_version": "v1alpha"})

# Define a route for the web service
@app.route('/api', methods=['POST'])
def api():
    try:
        # Parse JSON input from the request
        data = request.json
        prompt = data.get('prompt', 'No prompt provided')

        # Generate content using GenAI
        config = {"thinking_config": {"include_thoughts": True}}
        response = client.models.generate_content(
            model="gemini-2.0-flash-thinking-exp-01-21",
            contents=prompt,
            config=config
        )

        # Format the response
        result = {"response": [], "thoughts": []}
        for part in response.candidates[0].content.parts:
            if part.thought:
                result["thoughts"].append(part.text)
            else:
                result["response"].append(part.text)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
