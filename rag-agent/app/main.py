import logging
from fastapi import FastAPI
from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Campus Help Assistant",
    description="A RAG-based chatbot for campus handbook queries",
    version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logging.getLogger(__name__).info("Campus Help Assistant started successfully")