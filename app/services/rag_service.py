from app.vector_store.chroma_client import collection
from app.services.embedding_service import generate_embeddings
from app.services.llm_service import generate_answer
from typing import List

class RAGService:
    def __init__(self, top_k: int = 5):
        """
        top_k: number of chunks to retrieve for context
        """
        self.top_k = top_k

    def retrieve_relevant_chunks(self, query: str, section_id: str) -> List[str]:
        """
        Retrieve top_k relevant document chunks from the vector DB filtered by section_id
        """
        # Generate embedding for the query
        query_embedding = generate_embeddings([query])[0]

        # Query the vector DB with section_id filter
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,  # Use self.top_k
            where={"section_id": section_id},  # Filter by section_id
            include=["documents", "metadatas"]
        )

        # Flatten documents and metadata for source tracking
        chunks = []
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            chunks.append(f"{doc} (source: {meta.get('source', 'unknown')})")

        return chunks

    def answer_question(self, question: str, section_id: str) -> dict:
        """
        Main method: retrieve context and ask LLM
        Returns a dictionary for JSON serialization
        """
        chunks = self.retrieve_relevant_chunks(question, section_id)
        context = "\n\n".join(chunks)  # Merge top-k chunks

        # Call LLM
        answer = generate_answer(context, question)
        
        # Return JSON-serializable dict instead of just string
        return {
            "answer": answer,
            "sources": chunks,
            "section_id": section_id,
            "context_chunks_count": len(chunks)
        }