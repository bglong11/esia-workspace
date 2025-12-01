"""Pydantic schemas for API request/response validation"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FactBase(BaseModel):
    signature: str
    name: str
    fact_type: str
    value_raw: Optional[str] = None
    value_num: Optional[float] = None
    unit_raw: Optional[str] = None
    value_normalized: Optional[float] = None
    unit_normalized: Optional[str] = None
    evidence: Optional[str] = None
    page: Optional[int] = None
    chunk_id: Optional[int] = None
    aliases: Optional[str] = None
    occurrence_count: int = 1
    has_conflict: bool = False
    conflict_description: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    user_edited: bool = False
    user_comment: Optional[str] = None
    # Factsheet categorization
    category: Optional[str] = None
    subcategory: Optional[str] = None
    categorization_confidence: Optional[str] = None
    categorization_rationale: Optional[str] = None


class FactResponse(FactBase):
    id: int
    job_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FactUpdate(BaseModel):
    """Schema for updating a fact"""
    value_normalized: Optional[float] = None
    unit_normalized: Optional[str] = None
    user_comment: Optional[str] = None
    user_edited: bool = True


class JobBase(BaseModel):
    session_id: str
    filename: str
    original_filename: str


class JobResponse(JobBase):
    id: int
    status: str
    progress: int
    total_chunks: int
    processed_chunks: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobWithFacts(JobResponse):
    facts: List[FactResponse] = []

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    job_id: int
    session_id: str
    message: str
    status: str
