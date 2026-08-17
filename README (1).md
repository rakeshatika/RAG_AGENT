# RAG Agent

A Retrieval-Augmented Generation (RAG) application that allows users to
ask questions over a collection of documents and receive context-aware
answers based on retrieved information.

## Overview

The project combines document retrieval with Large Language Model (LLM)
generation:

1.  Documents are loaded and processed.
2.  Text is split into smaller chunks.
3.  Chunks are converted into vector embeddings.
4.  Embeddings are stored in a vector database.
5.  A user submits a question.
6.  Relevant document chunks are retrieved.
7.  The retrieved context is passed to the LLM.
8.  The application generates a grounded answer.

## Key Features

-   Document-based question answering
-   Semantic/vector search
-   Retrieval-Augmented Generation
-   Context-aware responses
-   REST API using FastAPI
-   Configurable application settings
-   Retrieval and generation service separation
-   Automated tests for core retrieval functionality
-   Environment-based configuration for API credentials

## Technology Stack

-   **Language:** Python
-   **API:** FastAPI
-   **RAG / LLM:** LangChain, LLM API
-   **Embeddings:** Sentence Transformers
-   **Vector Store:** ChromaDB
-   **Testing:** Pytest
-   **Environment:** Python virtual environment
-   **Version Control:** Git and GitHub

## Project Structure

``` text
RAG_AGENT/
│
├── .gitignore
├── README.md
│
└── rag-agent/
    ├── app/
    │   ├── api/
    │   ├── core/
    │   ├── services/
    │   └── ...
    │
    ├── tests/
    │   └── test_retrieval_service.py
    │
    ├── requirements.txt
    └── ...
```

> The exact package structure may vary depending on the current
> implementation.

## Prerequisites

Install the following before running the project:

-   Python 3.10+
-   pip
-   Git
-   An LLM API key if the configured model requires one

## Installation

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd RAG_AGENT
```

### 2. Create a virtual environment

Windows:

``` cmd
python -m venv .venv
```

### 3. Activate the virtual environment

Windows Command Prompt:

``` cmd
.venv\Scripts\activate
```

PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

If `requirements.txt` is inside `rag-agent`:

``` cmd
cd rag-agent
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file and add the required configuration.

Example:

``` env
LLM_API_KEY=your_api_key_here
```

Do not commit `.env` or API keys to GitHub.

The project `.gitignore` should contain:

``` gitignore
.venv/
__pycache__/
*.pyc
.env
.vscode/
```

## Running the Application

From the application directory, start the FastAPI server with:

``` cmd
uvicorn api.main:app --reload --port 8000
```

The API will normally be available at:

``` text
http://localhost:8000
```

FastAPI interactive documentation:

``` text
http://localhost:8000/docs
```

## RAG Workflow

``` text
                ┌─────────────────┐
                │     Documents   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Extraction │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Chunking        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Embeddings      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Vector Store    │
                └────────┬────────┘
                         │
                    User Question
                         │
                         ▼
                ┌─────────────────┐
                │ Similarity      │
                │ Retrieval       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Retrieved       │
                │ Context         │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ LLM Generation  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Final Answer    │
                └─────────────────┘
```

## Testing

Run the test suite from the application directory:

``` cmd
pytest
```

For a specific retrieval test:

``` cmd
pytest tests/test_retrieval_service.py
```

## API Documentation

After starting the FastAPI server, open:

``` text
http://localhost:8000/docs
```

This provides Swagger UI for exploring and testing the available API
endpoints.

## Important Git Notes

The following files and directories should not be committed:

-   `.venv/`
-   `.env`
-   `__pycache__/`
-   Python `.pyc` files
-   Local IDE configuration when not required

Check the repository before pushing:

``` cmd
git status
```

Then:

``` cmd
git add .
git commit -m "Initial commit"
git push -u origin main
```

## Security

Never place API keys directly inside Python source code.

Use environment variables instead:

``` python
import os

api_key = os.getenv("LLM_API_KEY")
```

If a secret is accidentally committed, rotate/revoke the exposed
credential immediately and remove the secret from the repository history
before making the repository public.

## Future Improvements

-   Add support for more document formats
-   Improve chunking and retrieval strategies
-   Add metadata filtering
-   Add conversation memory
-   Add authentication and authorization
-   Add a frontend interface
-   Add streaming responses
-   Add retrieval evaluation metrics
-   Add Docker deployment
-   Deploy the API to a cloud platform

## Learning Outcomes

This project demonstrates practical experience with:

-   Python backend development
-   FastAPI REST APIs
-   RAG architecture
-   Vector embeddings
-   Semantic search
-   Vector databases
-   LLM integration
-   Prompt construction
-   Automated testing
-   Git and GitHub

## License

This project is intended for learning and portfolio purposes.
