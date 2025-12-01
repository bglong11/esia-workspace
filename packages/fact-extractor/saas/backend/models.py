"""Database models for ESIA Fact Extractor SaaS"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Job(Base):
    """Represents a PDF processing job"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    progress = Column(Integer, default=0)  # 0-100
    total_chunks = Column(Integer, default=0)
    processed_chunks = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facts = relationship("Fact", back_populates="job", cascade="all, delete-orphan")


class Fact(Base):
    """Represents an extracted fact from a document"""
    __tablename__ = "facts"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)

    # Fact identification
    signature = Column(String(255), index=True, nullable=False)
    name = Column(String(500), nullable=False)
    fact_type = Column(String(50), default="quantity")  # quantity or categorical

    # Values
    value_raw = Column(String(255))
    value_num = Column(Float)
    unit_raw = Column(String(100))
    value_normalized = Column(Float)
    unit_normalized = Column(String(100))

    # Context
    evidence = Column(Text)
    page = Column(Integer)
    chunk_id = Column(Integer)
    aliases = Column(Text)  # Semicolon-separated list

    # Conflict tracking
    occurrence_count = Column(Integer, default=1)
    has_conflict = Column(Boolean, default=False)
    conflict_description = Column(Text, nullable=True)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)

    # User edits
    user_edited = Column(Boolean, default=False)
    user_comment = Column(Text, nullable=True)

    # Factsheet categorization
    category = Column(String(100), nullable=True)
    subcategory = Column(String(100), nullable=True)
    categorization_confidence = Column(String(20), nullable=True)  # high, medium, low
    categorization_rationale = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    job = relationship("Job", back_populates="facts")
