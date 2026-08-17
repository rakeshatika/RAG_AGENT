from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str


class RetrievedSource(BaseModel):
    chunk_id: str
    section_title: str
    source_file: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[RetrievedSource]
    retrieved_chunks_count: int


class Chunk(BaseModel):
    chunk_id: str
    section_title: str
    text: str
    source_file: str