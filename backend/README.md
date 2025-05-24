# JAMCare Virtual Health Assistant Backend

This is the FastAPI backend for the JAMCare Virtual Health Assistant, powered by OpenAI GPT-4o-mini. It is designed for compliance with Jamaican and international health data regulations.

## Features
- Secure, compliant chat endpoint using OpenAI GPT-4o-mini
- SYSTEM prompt enforces safety, privacy, and clinical guardrails
- Ready for RAG (retrieval-augmented generation) and audit logging

## Setup
1. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   uvicorn main:app --reload
   ```

## API
- `POST /chat` with JSON `{ "message": "...", "chat_id": "...", "consent": true }`
- Returns `{ "answer": "..." }`

## Compliance
- No PII is collected unless for nurse call-back.
- Only chat ID, timestamp, and consent flag are logged (future implementation).
- All data is treated as "special category" under Jamaica Data Protection Act 2020.
- See `main.py` for full SYSTEM prompt and compliance logic.

## Next Steps
- Add frontend (React, mobile-first, accessible)
- Implement audit logging and nurse call-back
- Integrate RAG for guideline-based answers 