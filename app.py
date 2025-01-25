from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("The GENAI_API_KEY environment variable is not set.")

app = Flask(__name__)

# Define the root route
@app.route('/')
def home():
    return render_template('index.html')

# Define the API route
@app.route('/api', methods=['POST'])
def api():
    try:
        # Get the JSON data from the request
        data = request.json
        prompt = data.get('prompt', 'No prompt provided')

        # Simulate AI response (replace this with your actual logic)
        response = f"You entered: {prompt}"

        return response, 200

    except Exception as e:
        return str(e), 500

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)