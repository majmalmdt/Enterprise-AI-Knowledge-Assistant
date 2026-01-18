from openai import OpenAI
from app.core.config import OPENAI_API_KEY, MODEL_NAME

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(context: str, question: str) -> str:
    """
    Sends a prompt to the LLM and returns the answer.
    - context: the retrieved document chunks
    - question: user's query
    """

    # Prepare prompt with clear instructions
    prompt = f"""
You are a knowledge assistant. Answer the question using only the context below. 
If the answer is not in the context, reply: "I don't know."

Context:
{context}

Question:
{question}
"""

    # Call OpenAI ChatCompletion API
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # deterministic answer
    )

    return response.choices[0].message.content
