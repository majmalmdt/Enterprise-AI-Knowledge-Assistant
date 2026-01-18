from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PERSIST_DIR = BASE_DIR / "chroma_db"

PERSIST_DIR.mkdir(parents=True, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=str(PERSIST_DIR))

collection = chroma_client.get_or_create_collection(name="knowledge_collection")

