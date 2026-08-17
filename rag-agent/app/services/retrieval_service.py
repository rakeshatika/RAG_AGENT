def retrieve_relevant_chunks(question: str, top_k: int = None) -> list:
    if top_k is None:
        top_k = settings.TOP_K

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    collection = get_chroma_collection() # type: ignore
    count = collection.count()

    if count == 0:
        raise RuntimeError("Vector store is empty. Run ingestion first.")

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, count)
    )

    chunks = []

    # Maximum allowed distance.
    # Lower distance means higher similarity.
    MAX_DISTANCE = 0.55

    if results and results["documents"] and results["documents"][0]:

        for i, doc in enumerate(results["documents"][0]):

            metadata = results["metadatas"][0][i]

            distance = (
                results["distances"][0][i]
                if results.get("distances")
                else None
            )

            # Ignore irrelevant chunks
            if distance is None or distance > MAX_DISTANCE:
                logger.info( # type: ignore
                    "Skipped irrelevant chunk: %s | distance=%.4f",
                    metadata.get("section_title"),
                    distance if distance is not None else -1
                )
                continue

            chunks.append({
                "chunk_id": metadata.get(
                    "chunk_id",
                    f"chunk_{i+1}"
                ),
                "section_title": metadata.get(
                    "section_title",
                    "Unknown"
                ),
                "source_file": metadata.get(
                    "source_file",
                    "campus_handbook.txt"
                ),
                "text": doc,
                "distance": distance
            })

            logger.info( # type: ignore
                "Retrieved relevant chunk: %s | distance=%.4f",
                metadata.get("section_title"),
                distance
            )

    return chunks