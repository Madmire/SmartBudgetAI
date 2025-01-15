

from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "open_api")

# Initialisation de l'application FastAPI
app = FastAPI(title="SmartBudgetAI Chatbot API")

# Schéma de requête
class ChatRequest(BaseModel):
    prompt: str

# Endpoint pour obtenir une réponse de l'API OpenAI
@app.post("/chat")
async def get_response(request: ChatRequest):
    try:
        # Appel à l'API OpenAI
        response = openai.ChatCompletion.acreate(
            model="gpt-4o-mini",  # Utilisez "gpt-4" si disponible
            messages=[
                {"role": "system", "content": "Tu es un expert en finances personnelles pour étudiants. Donne des conseils précis et adaptés aux situations courantes des étudiants."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=0.9,
        )

        # Extraire et renvoyer la réponse
        answer = (await response).choices[0].message.content.strip()
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}

# Endpoint pour tester si le serveur fonctionne
@app.get("/")
def read_root():
    return {"message": "SmartBudgetAI Chatbot API fonctionne avec OpenAI !"}
