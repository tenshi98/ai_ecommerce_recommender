"""Modelo de respuesta del recomendador de productos."""
from pydantic import BaseModel, Field


class RecommendationResponse(BaseModel):
    """Recomendaciones generadas por el modelo."""

    recommendations: str = Field(..., description="Productos sugeridos por Ollama.")
