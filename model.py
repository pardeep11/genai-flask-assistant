import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Dynamic package imports based on availability/choice
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# Added GEMINI_API_KEY to the imported configurations
from config import PARAMETERS, OLLAMA_BASE_URL, GEMINI_MODEL_ID, LOCAL_LLAMA_MODEL_ID, GEMINI_API_KEY

# Define JSON output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

# JSON output parser
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# Initialize standard Chat Prompt Template
# Eliminates IBM/Model-specific template syntax so it works seamlessly on Gemini & Ollama
chat_template = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}\n\n{format_prompt}"),
    ("human", "{user_prompt}")
])

# Model Initialization Functions
def get_gemini_model():
    """Initializes Google Gemini Model with securely loaded API key"""
    if not GEMINI_API_KEY:
        raise ValueError("CRITICAL: GEMINI_API_KEY is missing or could not be loaded from configuration!")
        
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL_ID,
        temperature=PARAMETERS["temperature"],
        max_tokens=PARAMETERS["max_tokens"],
        api_key=GEMINI_API_KEY  # Securely injected from config.py
    )

def get_local_model(model_id):
    """Initializes Local Ollama Model"""
    return ChatOllama(
        model=model_id,
        base_url=OLLAMA_BASE_URL,
        temperature=PARAMETERS["temperature"],
        num_predict=PARAMETERS["max_tokens"]
    )

# Execution Core
def get_ai_response(model, system_prompt, user_prompt):
    chain = chat_template | model | json_parser
    return chain.invoke({
        'system_prompt': system_prompt, 
        'user_prompt': user_prompt, 
        'format_prompt': json_parser.get_format_instructions()
    })

# Unified Engine wrappers for your Flask App routes
def gemini_response(system_prompt, user_prompt):
    model = get_gemini_model()
    return get_ai_response(model, system_prompt, user_prompt)

def local_llama_response(system_prompt, user_prompt):
    model = get_local_model(LOCAL_LLAMA_MODEL_ID)
    return get_ai_response(model, system_prompt, user_prompt)