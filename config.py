import os
import json

# Model parameters
PARAMETERS = {
    "temperature": 0.1,
    "max_tokens": 256,
}

# Local Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Model IDs
GEMINI_MODEL_ID = "gemini-2.5-flash"
LOCAL_LLAMA_MODEL_ID = "llama3.1:8b"

def get_secure_credential(key_name, default_value=None):
    """
    Checks the current working directory first (Project Root), 
    then checks relative to config.py to ensure credentials.json is found.
    """
    # Path 1: Project Root Directory (Where app.py or terminal runs)
    root_path = os.path.join(os.getcwd(), "credentials.json")
    
    # Path 2: Subfolder Directory (Where config.py lives)
    config_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
    
    # Select whichever file actually exists
    if os.path.exists(root_path):
        target_file = root_path
    elif os.path.exists(config_dir_path):
        target_file = config_dir_path
    else:
        # Fallback to system environment if file is totally missing
        return os.getenv(key_name, default_value)
        
    try:
        with open(target_file, "r") as f:
            data_keys = json.load(f)
            # Fetch directly using dictionary lookup .get()
            return data_keys.get(key_name, default_value)
    except (json.JSONDecodeError, IOError):
        return os.getenv(key_name, default_value)

# Dynamically resolve the Gemini key at configuration runtime
GEMINI_API_KEY = get_secure_credential("google_api_key")