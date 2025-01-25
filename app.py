from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Ensure API key exists
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("The GENAI_API_KEY environment variable is not set.")

# Initialize Flask app
app = Flask(__name__)

# Initialize GenAI client
try:
    client = genai.Client(api_key=GENAI_API_KEY, http_options={"api_version": "v1alpha"})
except Exception as e:
    raise RuntimeError(f"Failed to initialize GenAI client: {str(e)}")

# Root route
@app.route('/')
def home():
    return render_template('index.html')

# API route to process input and generate a response
@app.route('/api', methods=['POST'])
def api():
    try:
        # Parse the JSON input
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return "No prompt provided", 400

        # Call the AI model
        config = {"temperature": 0.7}
        print(f"Sending prompt to AI: {prompt}")  # Debug log
        ai_response = client.models.generate_content(
            model="gemini-exp-1206",  # Corrected model ID
            contents=prompt,
            config=config
        )

        # Extract the response text
        response_text = ai_response.candidates[0].content.parts[0].text
        print(f"AI response: {response_text}")  # Debug log

        # Return the response as plain text
        return response_text, 200

    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error
        return f"Server error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
