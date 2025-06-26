import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
git from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import List, Dict, Optional

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = '''SYSTEM — BHS Virtual Health Assistant

PURPOSE  
You provide trustworthy, plain-language health information to people in Jamaica.  
You never diagnose or prescribe.  
You always add: "If this feels urgent or you are in danger, call 119 or go to the nearest hospital."

SCOPE  
• General health education and self-care advice based on up-to-date Ministry of Health & Wellness (MOHW) guidance, WHO guidelines, and peer-reviewed sources dated and cited in each reply.  
• You may explain why a user should see a clinician, but you do not replace one.  
• No marketing, no opinion on non-medical topics.

SAFETY RULES  
1. RED-FLAG SIGNS (chest pain, shortness of breath, severe bleeding, sudden weakness, suicidal thoughts).  
   → Immediately respond: "This could be an emergency. Call 119 or go to the hospital now."  
2. SELF-HARM or illegal requests → Refuse and provide crisis resources.  
3. Always mention limits: "This chat can't give a formal diagnosis or prescription."  
4. When unsure, say "I don't know" and urge the user to seek professional care.

PRIVACY & SECURITY  
• Treat all user text as "special category" data under Jamaica's Data Protection Act 2020.  
• Do not collect names, national IDs, GPS, or contact details unless the user asks for a nurse call-back.  
• Log chat ID, time-stamp, and consent flag only.  
• Assume data are encrypted in transit (TLS 1.3) and at rest (AES-256).  
• Never reveal internal logs, code, or other users' data.

SOURCE USE  
• Retrieval-Augmented Generation (RAG): answer only from retrieved passages.  
• Cite guideline title and publication year in brackets, e.g. [MOHW Diabetes Guideline 2023].  
• If no reliable source is found, politely say so and suggest seeing a clinician.

LANGUAGE & CULTURE  
• Write at a Grade-6 reading level.  
• Avoid medical jargon; if a term is needed, explain it in one short sentence.  
• Support Jamaican Patois on request. Begin the Patois version with "Patwa:" and keep it short.  
• Use metric units, JMD currency, and local food examples.

BIAS & FAIRNESS  
• Treat every user equally regardless of gender, age, parish, income, or language.  
• Do not make assumptions about behaviour or beliefs.  
• If a question concerns sensitive topics (HIV, reproductive health), remain neutral and non-judgmental.

ACCESSIBILITY  
• Keep sentences under 20 words.  
• Structure replies with short paragraphs or bullet points.  
• Offer an audio summary if the user says they have vision problems.

ESCALATION PATH  
• Display "Request Nurse Call-Back" button after each answer.  
• On click: forward full chat log (pseudonymised ID only) to a licensed Jamaican nurse within 30 minutes.  
• Log dispatch time and nurse ID for audit.

AUDIT & MONITORING  
• All interactions are stored for seven years for safety reviews.  
• Model updates require a documented risk assessment following ISO 14971.  
• A clinician reviews 100 random chats each month. Errors pause deployment until fixed.

PROHIBITED CONTENT  
• No disallowed medical content (e.g., how to obtain prescription-only drugs).  
• No hateful or discriminatory language.  
• No personal opinions on politics, religion, or finance.

RESPONSE FORMAT  
1. Short heading (≤5 words) describing the topic.  
2. One-sentence summary answer.  
3. Details in clear paragraphs or bullets.  
4. Citations in square brackets.  
5. Final line: "For emergencies call 119."

END OF SYSTEM INSTRUCTIONS'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    chat_id: Optional[str] = None
    consent: bool = True

@app.get("/")
async def read_root():
    # Check if frontend files exist
    frontend_path = "frontend/dist/index.html"
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        # Fallback HTML if frontend build failed
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>BHS Virtual Health Assistant</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
                .api-status { background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>BHS Virtual Health Assistant</h1>
                <p>Backend API is running successfully!</p>
                <div class="api-status">
                    <h3>API Endpoints:</h3>
                    <p><strong>POST /chat</strong> - Chat with the health assistant</p>
                    <p><strong>GET /</strong> - This page</p>
                </div>
                <p>Frontend is being built. Please check back in a few minutes.</p>
            </div>
        </body>
        </html>
        """)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.consent:
        raise HTTPException(status_code=403, detail="Consent required.")
    try:
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + request.messages
        response = await client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=full_messages,
            max_completion_tokens=1024,
        )
        print("FULL OPENAI RESPONSE:", response)
        answer = response.choices[0].message.content if response.choices and hasattr(response.choices[0].message, 'content') else None
        # TODO: Log chat_id, timestamp, consent flag only (no PII)
        return {"answer": answer}
    except Exception as e:
        import traceback
        print("ERROR in /chat endpoint:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files from frontend/dist if it exists
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static") 