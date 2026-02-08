from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # ou le chemin local de ton modèle
vec = model.encode(["Ceci est un test"])
print(vec[0][:10])  # les 10 premières valeurs du vecteur
