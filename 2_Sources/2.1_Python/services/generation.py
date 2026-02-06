from pathlib import Path
from datetime import datetime
import subprocess
from .vector_store import search_similar
from docx import Document

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "5_Outputs" / "DOCX"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_document(prompt: str, template: str = "default"):
    """
    Récupère des documents similaires depuis Chroma et génère un document avec Ollama
    """
    # Recherche des documents similaires
    docs = search_similar(prompt, k=3)
    context = "\n\n".join([d["text"] for d in docs])

    # Construire le prompt complet pour Ollama
    full_prompt = f"Contexte:\n{context}\n\nPrompt:\n{prompt}"

    # Nom du fichier de sortie
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    output_file = OUTPUT_DIR / f"Document_{template}_{timestamp}.docx"

    # Appel de Ollama (exemple avec Mistral-7B)
    result = subprocess.run(
        ["ollama", "generate", "Mistral-7B", full_prompt],
        capture_output=True,
        text=True
    )
    generated_text = result.stdout

    # Écriture dans un DOCX
    doc = Document()
    doc.add_paragraph(generated_text)
    doc.save(output_file)

    return f"Document {output_file.name} généré avec le prompt: {prompt}"
