# Enterprise Hybrid GenAI Assistant (Flask + LangChain)

A simple AI chat assistant built with **Flask**, **LangChain**, **Google Gemini 2.5 Flash**, and **Ollama (Llama 3.1)**. It supports both cloud and local LLMs and returns structured JSON responses using Pydantic.
<img width="969" height="776" alt="image" src="https://github.com/user-attachments/assets/95791e0b-4cdc-45ad-967c-047a34e3d0a2" />
<img width="1117" height="594" alt="image" src="https://github.com/user-attachments/assets/a695a1a6-9735-4ef0-ae0f-ee66b30a24ec" />



---

## Features

* Switch between **Google Gemini 2.5 Flash** and **Ollama (Llama 3.1)**.
* Structured JSON responses using **Pydantic**.
* Response includes:

  * **summary** – User query summary
  * **sentiment** – Score from 0 to 100
  * **response** – AI-generated answer
* Automatically parses JSON responses from LLMs.
* Secure API key management using `credentials.json`.
* Simple and responsive chat interface.
* CORS enabled for frontend-backend communication.

---

## Project Architecture

```
Frontend (HTML, CSS, JavaScript)
            │
            ▼
      Flask Backend
            │
      LangChain
            │
    ┌───────┴────────┐
    ▼                ▼
Google Gemini    Ollama (Llama 3.1)
```

---

## Tech Stack

* Python
* Flask
* LangChain
* Google Gemini API
* Ollama
* Pydantic
* HTML
* CSS
* JavaScript

---

## Installation

### 1. Clone the Repository

```bash
git@github.com:pardeep11/genai-flask-assistant.git
cd genai-flask-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Credentials

Create a `credentials.json` file in the project root.

```json
{
    "google_api_key": "YOUR_GEMINI_API_KEY",
    "ollama_base_url": "http://localhost:11434"
}
```

> This file is ignored by Git using `.gitignore`.

### 5. Run Ollama

```bash
ollama pull llama3.1:8b
ollama serve
```

### 6. Start the Flask Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## Project Structure

```
genai-flask-assistant/
│
├── app.py
├── model.py
├── config.py
├── templates/
├── static/
├── credentials.json      # Not committed
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Security

* `credentials.json` is excluded from Git.
* API keys are not hardcoded.
* CORS is enabled for safe frontend communication.

---

## Future Improvements

* Docker support
* Chat history
* Streaming responses
* Multiple LLM providers
* Authentication
