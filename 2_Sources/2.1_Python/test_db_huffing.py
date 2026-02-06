from sentence_transformers import SentenceTransformer
model = SentenceTransformer("3_Data/models/huggingface_embeddings/all-MiniLM-L6-v2")
embeddings = model.encode(["Bonjour le monde"])
print(embeddings[0][:10])  # les 10 premières valeurs
