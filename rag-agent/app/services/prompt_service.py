import logging

logger = logging.getLogger(__name__)

NO_ANSWER_RESPONSE = (
    "I do not have enough information in the provided knowledge base to answer that."
)

# Distance threshold — ChromaDB uses L2 distance; lower = more similar
RELEVANCE_THRESHOLD = 1.5


def is_relevant(chunks: list) -> bool:
    """Check if retrieved chunks are relevant enough to answer."""
    if not chunks:
        return False
    
    # If distance scores are available, check the best one
    distances = [c.get("distance") for c in chunks if c.get("distance") is not None]
    if distances:
        best_distance = min(distances)
        logger.info(f"Best retrieval distance: {best_distance:.4f} (threshold: {RELEVANCE_THRESHOLD})")
        return best_distance < RELEVANCE_THRESHOLD
    
    # If no distances, assume relevant
    return True


def build_prompt(question: str, chunks: list) -> list:
    """Build the prompt messages for the LLM."""
    context_parts = []
    for chunk in chunks:
        context_parts.append(
            f"[{chunk['section_title']}]\n{chunk['text']}"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    system_message = (
        "You are a helpful campus assistant. "
        "Answer ONLY from the provided context below. "
        "If the answer is not in the context, say exactly: "
        "\"I do not have enough information in the provided knowledge base to answer that.\" "
        "Keep your answer concise and mention the source section when possible."
    )
    
    user_message = (
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    logger.info(f"Built prompt with {len(chunks)} context chunks")
    return messages