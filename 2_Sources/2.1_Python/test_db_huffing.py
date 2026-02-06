import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone


# =========================
# CONFIG (doit matcher ton env)
# =========================

CHROMA_PERSIST_DIR = os.environ.get(
    "CHROMA_PERSIST_DIR",
    "/mnt/data1_100g/agent_llm_local/vectors"
)

MODEL_PATH = os.environ.get(
    "SENTENCE_TRANSFORMERS_HOME",
    "/mnt/data1_100g/agent_llm_local/models/sentence-transformers"
)

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "test_huffing"

print("CHROMA_PERSIST_DIR =", CHROMA_PERSIST_DIR)
print("MODEL_PATH =", MODEL_PATH)

# =========================
# LOAD MODEL (singleton local)
# =========================

model = SentenceTransformer(
    model_name_or_path=MODEL_NAME,
    cache_folder=MODEL_PATH
)

print("Embedding model loaded")

# =========================
# INIT CHROMA CLIENT
# =========================

client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PERSIST_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"description": "Test huffing embeddings"}
)

print(f"Collection '{COLLECTION_NAME}' ready")

# =========================
# TEST DATA
# =========================

texts = [
    "NoXoZ est un projet d'agent LLM local.",
    "Les embeddings permettent la recherche sémantique.",
    "ChromaDB stocke des vecteurs persistants.",
    "FastAPI expose une API pour le système."
]

metadatas = [
    {"source": "manual", "idx": i, "created_at": datetime.now(timezone.utc).isoformat()}
    for i in range(len(texts))
]

ids = [f"test_{i}" for i in range(len(texts))]

# =========================
# EMBEDDING + INSERTION
# =========================

embeddings = model.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

# client.persist()

print("Documents embedded and persisted")

# =========================
# QUERY TEST
# =========================

query = "Comment fonctionne la recherche sémantique ?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print("\nQUERY:", query)
print("\nRESULTS:")
for i, doc in enumerate(results["documents"][0]):
    print(f"- {doc}")
    print(f"  metadata: {results['metadatas'][0][i]}")

print("\nTEST OK")
