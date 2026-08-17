import sys
import os
import logging

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_ingestion():
    from app.services.ingestion_service import (
        read_raw_file,
        split_into_chunks,
        save_chunks_to_json
    )
    from app.services.retrieval_service import store_chunks_in_vector_store

    RAW_FILE = "data/raw/campus_handbook.txt"
    CHUNKS_FILE = "data/processed/chunks.json"

    logger.info("=" * 50)
    logger.info("Starting ingestion pipeline...")
    logger.info("=" * 50)

    # Step 1: Read raw file
    logger.info("Step 1: Reading raw handbook file...")
    text = read_raw_file(RAW_FILE)
    logger.info(f"  Read {len(text)} characters")

    # Step 2: Split into chunks
    logger.info("Step 2: Splitting into chunks...")
    chunks = split_into_chunks(text)
    logger.info(f"  Created {len(chunks)} chunks:")
    for c in chunks:
        logger.info(f"    - {c['chunk_id']}: {c['section_title']}")

    # Step 3: Save chunks.json
    logger.info("Step 3: Saving chunks to JSON...")
    save_chunks_to_json(chunks, CHUNKS_FILE)
    logger.info(f"  Saved to {CHUNKS_FILE}")

    # Step 4: Generate embeddings & store in vector store
    logger.info("Step 4: Generating embeddings and storing in vector store...")
    logger.info("  (This may take a few seconds — calling OpenAI Embeddings API)")
    store_chunks_in_vector_store(chunks)
    logger.info("  Done!")

    logger.info("=" * 50)
    logger.info("✅ Ingestion complete! Chatbot is ready.")
    logger.info("=" * 50)


if __name__ == "__main__":
    run_ingestion()