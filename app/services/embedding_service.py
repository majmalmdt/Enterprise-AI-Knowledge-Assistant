from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_embeddings(texts: list[str]):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]
