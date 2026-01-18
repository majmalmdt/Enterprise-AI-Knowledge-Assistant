from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )

    filename = Column(String, nullable=False)
    content_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    section = relationship("Section", back_populates="files")

    chunks = relationship(
        "Chunk",
        back_populates="file",
        cascade="all, delete-orphan"
    )
