import json
import re
from flask import Flask, request, jsonify, render_template
from model import gemini_response, local_llama_response
import time

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    """
    Manually injects CORS headers into every response. 
    This prevents 'Failed to fetch' issues if the frontend is run 
    separately or opened directly as a file.
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    # Handle preflight OPTIONS requests from browsers smoothly
    if request.method == 'OPTIONS':
        return jsonify({"status": "preflight_ok"}), 200

    data = request.json or {}
    user_message = data.get('message')
    model = data.get('model')
    print(f"DEBUG: Selected model -> {model}")
    
    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    
    system_prompt = "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response."
    
    start_time = time.time()
    
    try:
        if model == 'ollama3':
            result = local_llama_response(system_prompt, user_message)
        elif model == 'gemini':
            result = gemini_response(system_prompt, user_message)
        else:
            return jsonify({"error": "Invalid model selection"}), 400
        
        # --- ROBUST PARSING PATCH ---
        if isinstance(result, str):
            cleaned = result.strip()
            
            # Use Regex to extract the outer-most curly braces { ... }
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(0)
            
            try:
                result = json.loads(cleaned)
            except Exception:
                result = {
                    "summary": "AI Response",
                    "sentiment": 70,
                    "response": result  # Fallback to display raw output on the screen
                }
        # --- END PATCH ---

        result['duration'] = time.time() - start_time
        return jsonify(result)
        
    except Exception as e:
        print(f"CRITICAL BACKEND ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)