import uuid
from fastapi import UploadFile, File, Depends, APIRouter,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.file import File as DBFile
from app.models.chunk import Chunk
from app.utils.file_loader import extract_text_from_pdf
from app.utils.chunker import chunk_text
from app.services.vector_service import save_to_vector_db, delete_from_vector_db_by_document

router = APIRouter()
@router.post("/{section_id}/upload")
async def upload_file_to_section(
    section_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    db_file = DBFile(
        section_id=section_id,
        filename=file.filename,
        content_type=file.content_type
    )

    db.add(db_file)
    await db.flush()  # 🔑 get file_id

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        db.add(
            Chunk(
                section_id=section_id,
                file_id=db_file.id,
                chunk_index=i,
                content=chunk
            )
        )

    await db.commit()

    save_to_vector_db(chunks, str(db_file.id,), str(section_id))
    return {
        "file_id": str(db_file.id),
        "chunks_added": len(chunks)
    }

@router.get("/{section_id}/files")
async def list_files_in_section(
    section_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DBFile).where(DBFile.section_id == section_id)
    )
    files = result.scalars().all()

    return [
        {
            "file_id": str(file.id),
            "filename": file.filename,
            "content_type": file.content_type,
            "uploaded_at": file.uploaded_at.isoformat()
        }
        for file in files
    ]

@router.get("/file/{file_id}/chunks")
async def get_chunks_of_file(
    file_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Chunk).where(Chunk.file_id == file_id).order_by(Chunk.chunk_index)
    )
    chunks = result.scalars().all()

    return [
        {
            "chunk_index": chunk.chunk_index,
            "content": chunk.content
        }
        for chunk in chunks
    ]

@router.delete("/file/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_and_chunks(
    file_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DBFile).where(DBFile.id == file_id)
    )
    db_file = result.scalar_one_or_none()

    if db_file:
        await db.delete(db_file)
        await db.commit()
        delete_from_vector_db_by_document(str(file_id), str(db_file.section_id))
    return {
        "message": "File and associated chunks deleted successfully.",
        "file_id": str(file_id)
    }