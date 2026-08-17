import os
import json
import re
import logging

logger = logging.getLogger(__name__)


def read_raw_file(filepath: str) -> str:
    """Read the raw handbook text file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Knowledge base file not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        raise ValueError(f"Knowledge base file is empty: {filepath}")
    
    logger.info(f"Successfully read file: {filepath}")
    return content


def split_into_chunks(text: str, source_file: str = "campus_handbook.txt") -> list:
    """Split handbook text into section-based chunks."""
    chunks = []
    
    # Split by "Section N:" pattern
    section_pattern = re.compile(r'(Section \d+:\s+[^\n]+)', re.IGNORECASE)
    parts = section_pattern.split(text)
    
    chunk_index = 1
    i = 1  # Start at 1 because split puts matches at odd indices
    
    while i < len(parts):
        header = parts[i].strip()         # e.g. "Section 1: Attendance Policy"
        body = parts[i + 1].strip() if (i + 1) < len(parts) else ""
        
        # Extract the section title (everything after "Section N: ")
        title_match = re.match(r'Section \d+:\s+(.+)', header)
        section_title = title_match.group(1).strip() if title_match else header
        
        full_text = f"{header}\n{body}"
        
        chunk = {
            "chunk_id": f"chunk_{chunk_index}",
            "section_title": section_title,
            "text": full_text,
            "source_file": source_file
        }
        chunks.append(chunk)
        chunk_index += 1
        i += 2
    
    logger.info(f"Created {len(chunks)} chunks from handbook")
    return chunks


def save_chunks_to_json(chunks: list, output_path: str) -> None:
    """Save chunks to a JSON file for traceability."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(chunks)} chunks to {output_path}")