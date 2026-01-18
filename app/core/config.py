from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
REDIS_URL = os.getenv("REDIS_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR")