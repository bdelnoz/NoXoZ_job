# services/generation.py

def generate_document(prompt: str, template: str = "default"):
    """
    Fonction placeholder pour génération de document.
    Retourne simplement un message simulant la création d'un document.
    """
    filename = f"output_{template}.docx"
    # Ici, tu pourras plus tard intégrer le LLM pour générer le document réel
    return f"Document {filename} généré avec le prompt: {prompt}"
