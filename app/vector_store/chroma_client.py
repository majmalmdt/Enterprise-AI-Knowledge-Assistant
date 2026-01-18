from pathlib import Path
import chromadb
from app.core.config import CHROMA_DB_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PERSIST_DIR = BASE_DIR / CHROMA_DB_DIR

PERSIST_DIR.mkdir(parents=True, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=str(PERSIST_DIR))

collection = chroma_client.get_or_create_collection(name="knowledge_collection")

