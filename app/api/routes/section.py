import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.section import Section

router = APIRouter()
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_section(
    name: str,
    db: AsyncSession = Depends(get_db)
):
    section = Section(name=name)

    db.add(section)
    await db.commit()
    await db.refresh(section)

    return {
        "id": str(section.id),
        "name": section.name
    }

@router.get("/")
async def list_sections(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Section))
    sections = result.scalars().all()

    return [
        {
            "id": str(section.id),
            "name": section.name
        }
        for section in sections
    ]

@router.get("/{section_id}")
async def get_section(
    section_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Section).where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    return {
        "id": str(section.id),
        "name": section.name
    }

@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Section).where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    await db.delete(section)
    await db.commit()
    return {
        "message": "Section deleted",
        "section_id": str(section_id)

    }