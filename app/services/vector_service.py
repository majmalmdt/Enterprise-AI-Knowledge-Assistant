from app.vector_store.chroma_client import chroma_client 
from app.vector_store.chroma_client import collection
from app.services.embedding_service import generate_embeddings
import uuid

def save_to_vector_db(chunks: list[str], document_name: str, section_id: str):
    embeddings = generate_embeddings(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": document_name, "section_id": section_id} for _ in chunks]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
def delete_from_vector_db_by_document(document_name: str, section_id: str):
    # Query to find all IDs with the given source
    results = collection.query(
        query_texts=[""],
        n_results=1000,  # assuming a max of 1000 chunks per document
        where={"source": document_name, "section_id": section_id},
        include=["ids"]
    )

    ids_to_delete = results['ids'][0]

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
