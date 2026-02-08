import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


# =========================
# CONFIG (doit matcher ton env)
# =========================

MODEL_PATH = Path(
    os.environ.get(
        "SENTENCE_TRANSFORMERS_HOME",
        "/mnt/data1_100g/agent_llm_local/models/sentence-transformers"
    )
)

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "test_huffing"


class TestChromaHuffing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CHROMA_AVAILABLE:
            raise unittest.SkipTest("chromadb/sentence_transformers non disponibles")

        if not MODEL_PATH.exists():
            raise unittest.SkipTest(
                f"Model path introuvable: {MODEL_PATH}. Définis SENTENCE_TRANSFORMERS_HOME."
            )

        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.model = SentenceTransformer(
            model_name_or_path=MODEL_NAME,
            cache_folder=str(MODEL_PATH)
        )

        cls.client = chromadb.Client(
            Settings(
                persist_directory=cls.temp_dir.name,
                anonymized_telemetry=False
            )
        )
        cls.collection = cls.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Test huffing embeddings"}
        )

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "temp_dir"):
            cls.temp_dir.cleanup()

    def test_query_returns_results(self):
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

        embeddings = self.model.encode(texts).tolist()
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        query = "Comment fonctionne la recherche sémantique ?"
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )

        self.assertEqual(len(results["documents"][0]), 3)
        self.assertEqual(len(results["metadatas"][0]), 3)


if __name__ == "__main__":
    unittest.main()
