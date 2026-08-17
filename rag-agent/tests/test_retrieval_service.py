from app.services import retrieval_service


def test_store_chunks_recovers_from_corrupt_collection(monkeypatch):
    class BadCollection:
        def get(self):
            raise TypeError("object of type 'int' has no len()")

        def delete(self, ids):
            self.deleted = ids

        def add(self, ids, documents, metadatas):
            self.added = {"ids": ids, "documents": documents, "metadatas": metadatas}

    class GoodCollection:
        def __init__(self):
            self.added = None

        def get(self):
            return {"ids": []}

        def delete(self, ids):
            self.deleted = ids

        def add(self, ids, documents, metadatas):
            self.added = {"ids": ids, "documents": documents, "metadatas": metadatas}

    calls = {"get_collection": 0, "reset": 0}

    def fake_get_chroma_collection():
        calls["get_collection"] += 1
        if calls["get_collection"] == 1:
            return BadCollection()
        return GoodCollection()

    def fake_reset_vector_store():
        calls["reset"] += 1

    monkeypatch.setattr(retrieval_service, "get_chroma_collection", fake_get_chroma_collection)
    monkeypatch.setattr(retrieval_service, "reset_vector_store", fake_reset_vector_store)

    chunks = [{"chunk_id": "1", "text": "hello", "section_title": "Intro", "source_file": "file.txt"}]

    retrieval_service.store_chunks_in_vector_store(chunks)

    assert calls["reset"] == 1
