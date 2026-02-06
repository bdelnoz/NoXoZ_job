# services/embeddings.py
from sentence_transformers import SentenceTransformer
import os

_MODEL = None

def get_embedding_model():
    global _MODEL
    if _MODEL is None:
        model_path = os.path.join(
            os.getenv("SENTENCE_TRANSFORMERS_HOME"),
            "all-MiniLM-L6-v2"
        )
        _MODEL = SentenceTransformer(model_path, device="cpu")
    return _MODEL

import torch

x = torch.tensor([1.0, 2.0, 3.0])
print(x * 2)

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # ou le chemin local de ton modèle
vec = model.encode(["Ceci est un test"])
print(vec[:1])  # les 10 premières valeurs du vecteur

import os
print("HF_HOME =", os.getenv("HF_HOME"))
print("SENTENCE_TRANSFORMERS_HOME =", os.getenv("SENTENCE_TRANSFORMERS_HOME"))
