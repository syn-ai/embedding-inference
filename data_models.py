from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from typing import Any, List

"""
This module defines the data models used throughout the embedding service.

It includes models for token usage, configuration, requests, and responses.
"""

class BaseModule(BaseModel, ABC):
    def __init__(self, **kwargs) -> None:
        def setattr(self, name: str, value: Any) -> None:
            return super().__setattr__(name, value)
        super().__init__(**kwargs)
        self.__setattr__ = setattr
        
    @abstractmethod
    async def process(self, url: str) -> Any:
        """Process a request made to the module."""


class TokenUsage(BaseModel):
    """Token usage model"""
    total_tokens: int = 0
    prompt_tokens: int = 0
    request_tokens: int = 0
    response_tokens: int = 0
    

class EmbeddingConfig(BaseModel):
    """
    Pydantic model for embedding-specific configuration.
    """
    port: int = Field(default=None)
    host: str = Field(default=None)
    endpoint: str = Field(default=None)

class Config(BaseModel):
    """
    Main configuration class using Pydantic BaseModel.
    """
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    version: str = Field(default=None)

    def update_config(self, kwargs: dict):
        """
        Update the configuration with new values.

        Args:
            kwargs (dict): Dictionary of configuration updates.
        """
        for key, value in kwargs.items():
            if isinstance(value, dict):
                if hasattr(self, key):
                    nested_config = getattr(self, key).model_validate(value)
                    setattr(self, key, nested_config)
            else:
                setattr(self, key, value)

class GenericRequest(BaseModel):
    data: str = Field(default_factory=str)
    
class EmbeddingRequest(BaseModel):
    text: str = Field(default_factory=str)
    
class EmbeddingResponse(JSONResponse):
    content: List[float] = Field(default_factory=List)