def generate_document(prompt: str, template: str = "default"):
    filename = f"output_{template}.docx"
    return f"Document {filename} généré avec le prompt: {prompt}"
