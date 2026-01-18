from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    files = relationship(
        "File",
        back_populates="section",
        cascade="all, delete-orphan"
    )

    chunks = relationship(
        "Chunk",
        back_populates="section",
        cascade="all, delete-orphan"
    )
