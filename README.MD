# Social Media Insights Analyzer

A chatbot that analyzes social media engagement data using Groq AI, Mistral embeddings, and Astra DB.

## Setup

1. Create virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with:
```
APP_TOKEN=your_token_here
```

4. Run app:
```bash
streamlit run app.py
```

## Technologies
- Langflow
- Groq AI
- Mistral AI Embeddings 
- DataStax Astra DB
- Streamlit