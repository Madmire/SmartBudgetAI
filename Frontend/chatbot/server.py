from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from transformers import GPTNeoForCausalLM, GPT2TokenizerFast
import logging

# Configurer la journalisation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser l'application FastAPI
app = FastAPI(title="SmartBudgetAI Chatbot API")

# Charger le modèle et le tokenizer GPT-Neo
try:
    model_name = "EleutherAI-gpt-neo-125M-finetuned"
    tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    model.eval()  # Passage en mode évaluation
    logger.info("Modèle et tokenizer chargés avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle ou du tokenizer : {str(e)}")
    raise RuntimeError(f"Erreur lors du chargement du modèle ou du tokenizer : {str(e)}")

# Définir le schéma de requête
class ChatRequest(BaseModel):
    prompt: str

def extract_response(full_text: str, prompt_text: str) -> str:
    """
    Extrait la réponse générée à partir du texte complet en retirant la portion du prompt.
    """
    if full_text.startswith(prompt_text):
        response = full_text[len(prompt_text):].strip()
    else:
        parts = full_text.split("[BOT]:")
        response = parts[-1].strip() if len(parts) > 1 else full_text.strip()
    return response

@app.post("/chat")
def get_response(request: ChatRequest):
    try:
        # Valider que le prompt n'est pas vide
        prompt_input = request.prompt.strip()
        if not prompt_input:
            raise HTTPException(status_code=400, detail="Le champ 'prompt' ne peut pas être vide.")

        # Construction du prompt en respectant le même format utilisé lors du fine-tuning
        prompt_text = (
            "[INSTRUCTION] Tu es un assistant expert en finances personnelles pour étudiants. "
            "Réponds de manière claire et utile à chaque question de l'utilisateur.\n\n"
            "[USER]: " + prompt_input + "\n[BOT]:"
        )
        logger.info(f"Prompt envoyé au modèle : {prompt_text}")

        # Préparer les entrées pour le modèle
        inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True)

        # Génération avec des paramètres adaptés
        output_ids = model.generate(
            **inputs,
            max_new_tokens=100,         # Génère jusqu'à 100 nouveaux tokens après le prompt
            min_new_tokens=30,          # Longueur minimale en tokens générés
            do_sample=True,            # Décodage déterministe (greedy) pour une meilleure cohérence
            temperature=0.7,            # Paramètre de température (peut être ajusté)
            top_p=0.2,                  # Nucleus sampling (peut être ajusté)
            repetition_penalty=1.2,     # Réduit les répétitions
            early_stopping=True,        # Arrête dès que la séquence semble complète
            pad_token_id=tokenizer.eos_token_id
        )

        # Décoder le texte généré
        full_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        logger.info(f"Texte généré par le modèle : {full_output}")

        # Extraire la réponse réelle (après la balise [BOT]:)
        response = extract_response(full_output, prompt_text)

        # Vérifier la longueur de la réponse pour s'assurer qu'elle est conséquente
        if len(response) < 10:
            logger.warning("Réponse générée trop courte ou incohérente.")
            raise HTTPException(status_code=500, detail="Réponse générée trop courte ou incohérente.")

        return {"answer": response}

    except ValidationError as ve:
        logger.error(f"Erreur de validation des données : {str(ve)}")
        raise HTTPException(status_code=422, detail=f"Erreur de validation des données : {str(ve)}")
    except Exception as e:
        logger.error(f"Erreur interne du serveur : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")

@app.get("/")
def read_root():
    return {"message": "SmartBudgetAI Chatbot API fonctionne avec GPT-Neo 125M !"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
