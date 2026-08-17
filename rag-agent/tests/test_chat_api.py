import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test 1: Health endpoint returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_valid_request():
    """Test 2: Chat endpoint accepts a valid request."""
    response = client.post("/chat", json={"question": "What is the attendance rule?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "retrieved_chunks_count" in data


def test_chat_endpoint_empty_question():
    """Test 3: Empty question is rejected with 422."""
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422


def test_known_question_returns_grounded_answer():
    """Test 4: Known question gets a grounded answer."""
    response = client.post("/chat", json={"question": "What is the revaluation fee?"})
    assert response.status_code == 200
    data = response.json()
    # Answer should mention 500 rupees
    assert "500" in data["answer"]
    assert len(data["sources"]) > 0


def test_unknown_question_returns_no_answer():
    """Test 5: Unknown question returns no-answer response."""
    response = client.post("/chat", json={"question": "Who is the principal of the college?"})
    assert response.status_code == 200
    data = response.json()
    assert "do not have enough information" in data["answer"].lower() or \
           "not" in data["answer"].lower()