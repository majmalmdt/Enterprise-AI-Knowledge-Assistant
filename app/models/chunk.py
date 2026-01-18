from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    section_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )

    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    section = relationship("Section", back_populates="chunks")
    file = relationship("File", back_populates="chunks")
