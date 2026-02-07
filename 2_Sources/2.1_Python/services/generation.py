from pathlib import Path
from datetime import datetime
import subprocess
from .vector_store import search_similar
from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "5_Outputs" / "DOCX"
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
        ["ollama", "run", "mistral:7b", "--", full_prompt],
        capture_output=True,
        text=True,
        timeout=120
    )
    if result.returncode != 0:
        error_detail = result.stderr.strip() or "Erreur inconnue Ollama"
        raise RuntimeError(f"Ollama a échoué: {error_detail}")
    generated_text = result.stdout.strip()
    if not generated_text:
        raise RuntimeError("Ollama n'a renvoyé aucun contenu.")

    # Écriture dans un DOCX
    doc = Document()
    doc.add_paragraph(generated_text)
    doc.save(output_file)

    return f"Document {output_file.name} généré avec le prompt: {prompt}"
