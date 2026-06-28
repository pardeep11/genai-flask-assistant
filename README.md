Enterprise Hybrid GenAI Assistant (Flask + LangChain)
A modern, responsive, and robust GenAI Chat Assistant that seamlessly bridges cloud-based Google Gemini 2.5 Flash and locally-hosted Ollama (Llama 3). Built using Flask, Pydantic, and LangChain, this application enforces structured JSON outputs (summary, sentiment, and response) while handling edge-case validation, CORS preflights, and directory resolution issues natively.
🚀 Key Features
Hybrid LLM Architecture: Instantly switch between high-speed cloud execution via Gemini 2.5 Flash and 100% free offline execution via local Ollama models.
Enforced Structured Schema: Utilizes Pydantic to guarantee that both cloud and local models return a strict JSON payload containing:
summary (str): Extraction of the user's inquiry.
sentiment (int): Normalized sentiment analysis scale from 0 (negative) to 100 (positive).
response (str): The structured, contextual assistant answer.
Robust Parsing Engine: Features an advanced regex parsing layer to strip unwanted markdown formats (e.g., ```json ... ```) and handle raw nested code outputs cleanly.
Secure Credentials Management: Implements an automated credential-loading dictionary that scans both current working directories and module-level paths, falling back gracefully to system environment variables.
Responsive Modern UI: Minimalist chat viewport using IBM Plex Sans typography, loading indicator transitions, run duration metrics, and auto-resizing textareas.
🛠️ System Architecture
                       +-------------------+
                       |    Frontend UI    |
                       |  (HTML, CSS, JS)  |
                       +---------+---------+
                                 |  JSON Post Request
                                 v
                       +---------+---------+
                       |   Flask Engine    | <---+ Dynamic CORS Injector
                       |    (app.py)       |
                       +---------+---------+
                                 |  Loads Configs
                                 v
                       +---------+---------+
                       |    config.py      | <---+ credentials.json (Gitignored)
                       +---------+---------+
                                 |  Orchestrates Chain
                                 v
                       +---------+---------+
                       |     model.py      |
                       +----+-----------+--+
                            |           |
       Cloud API Request    v           v    Local Loopback Port 11434
                +-----------+--+     +--+-----------+
                |    Google    |     |    Local     |
                |  Gemini 2.5  |     |   Ollama3    |
                +--------------+     +--------------+


📦 Tech Stack
Backend Framework: Python Flask
LLM Orchestration: LangChain Core, LangChain Google GenAI, LangChain Ollama
Data Validation: Pydantic (v2)
Frontend Layer: Vanilla JavaScript (ES6+), Tailwind CSS, Custom Responsive Viewport
🔌 Local Setup & Installation
1. Prerequisites
Python 3.10+ installed.
Ollama installed and running locally with your target model loaded:
ollama pull llama3.1:8b


2. Clone and Setup Environment
Clone this repository to your local directory:
git clone [https://github.com/YOUR_USERNAME/genai-flask-assistant.git](https://github.com/YOUR_USERNAME/genai-flask-assistant.git)
cd genai-flask-assistant


Create a single Python virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


Install the lightweight, highly optimized requirement stack:
pip install -r requirements.txt


3. Add Credentials (Local Dictionary Mode)
To protect your production keys, create a credentials.json file in your root folder. This file is automatically excluded from version control via .gitignore.
{
    "google_api_key": "YOUR_ACTUAL_GEMINI_API_KEY",
    "ollama_base_url": "http://localhost:11434"
}


4. Running the Application
Launch your development server:
python app.py


Open your browser and navigate to http://127.0.0.1:5000.
🐳 Docker Deployment
The application is completely packaged for containerization. You can easily build and run it using the lightweight slim-python container:
docker build -t genai-assistant .
docker run -p 5000:5000 --env-file .env genai-assistant


🔒 Security Best Practices
Git Protection: Your credentials.json and virtual environments are automatically blocked from public commit.
CORS Configuration: Configured with robust, explicit CORS preflight response headers to safely govern API communications across environments.
