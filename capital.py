import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

def get_credential(key_name, default_value=None):
    """
    Dynamically loads credentials.json as a dictionary and 
    fetches the requested key using the .get() method.
    """
    file_path = "credentials.json"
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Falling back to environment variables.")
        return os.getenv(key_name, default_value)
        
    try:
        with open(file_path, "r") as f:
            data_keys = json.load(f)
            return data_keys.get(key_name, default_value)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not valid JSON. Falling back to environment variables.")
        return os.getenv(key_name, default_value)

def test_inference(provider="gemini"):
    print(f"Testing inference using provider: {provider}")
    
    if provider == "gemini":
        # Dynamically fetch 'google_api_key' from the JSON dictionary
        api_key = get_credential("google_api_key")
        
        if not api_key:
            raise ValueError("Error: 'google_api_key' could not be resolved from credentials.json or system variables.")
        
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.0,
            api_key=api_key
        )
        
    elif provider == "ollama":
        # Dynamically fetch base URL or fallback to local default
        base_url = get_credential("ollama_base_url", "http://localhost:11434")
        model = ChatOllama(model="llama3.1:8b", base_url=base_url, temperature=0.0)
    
    messages = [
        SystemMessage(content="You are an expert assistant who provides concise and accurate answers. Only reply with the answer."),
        HumanMessage(content="What is the capital of Canada?")
    ]
    
    response = model.invoke(messages)
    print("Result:", response.content.strip())

if __name__ == "__main__":
    # Test your dynamic setup
    test_inference(provider="gemini")
