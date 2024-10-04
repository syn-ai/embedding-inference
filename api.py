"""
This module defines the FastAPI application for the embedding service.

It sets up the API endpoints, CORS middleware, and handles embedding requests.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from embedding.config import get_config
from embedding.embedding import get_embedding_module
from embedding.data_models import EmbeddingRequest, GenericRequest, EmbeddingResponse

from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
embedding = get_embedding_module()

config = get_config()

@app.post(f"{embedding.config.version}/{embedding.config.endpoint}")
async def create_embedding(request: GenericRequest):
    try:
        data = await request.model_dump_json()
        emebdding_request = EmbeddingRequest().model_validate(data)
        embedding = embedding.process(emebdding_request)
        return EmbeddingResponse(status_code=200, content=embedding)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host=config.embedding.host, port=config.embedding.port)

