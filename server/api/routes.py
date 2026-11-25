"""Rutas HTTP del servicio AI E-Commerce Product Recommender.

Expone la página de inicio y el endpoint ``/recommend``. La comunicación con
Ollama se delega en :class:`server.services.ollama.OllamaClient`, inyectado
por FastAPI.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse

from server.config import get_settings
from server.dependencies import OllamaClientDep
from server.schemas.responses import RecommendationResponse
from server.services.ollama import (
    OllamaClient,
    OllamaRequestError,
    OllamaResponseError,
)

logger = logging.getLogger(__name__)

router = APIRouter()
"""Enrutador con los endpoints públicos del servicio."""


@router.get("/", response_class=FileResponse, summary="Sirve la interfaz web")
def serve_homepage() -> FileResponse:
    """Devuelve el archivo ``static/index.html``.

    :returns: Respuesta con el HTML de la aplicación.
    :rtype: fastapi.responses.FileResponse
    """
    settings = get_settings()
    return FileResponse(settings.static_dir / "index.html")


def _generate_text(client: OllamaClient, prompt: str, fallback: str) -> str:
    """Genera texto y traduce los errores de Ollama a errores HTTP 500.

    :param client: Cliente de Ollama inyectado por FastAPI.
    :type client: server.services.ollama.OllamaClient
    :param prompt: Instrucción completa para el modelo.
    :type prompt: str
    :param fallback: Texto de reserva si la respuesta no trae ``response``.
    :type fallback: str
    :returns: Texto generado por el modelo.
    :rtype: str
    :raises fastapi.HTTPException: Con estado 500 si Ollama no responde o
        devuelve un cuerpo inválido.
    """
    try:
        return client.generate(prompt, fallback)
    except OllamaRequestError as exc:
        logger.error("Fallo al contactar con Ollama: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Request to Ollama failed: {exc}",
        ) from exc
    except OllamaResponseError as exc:
        logger.error("Respuesta inválida de Ollama: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Recomienda productos",
)
def recommend_products(
    client: OllamaClientDep,
    preferences: Annotated[str, Form(description="Preferencias de compra del usuario.")],
) -> RecommendationResponse:
    """Sugiere productos a partir de las preferencias del usuario.

    :param client: Cliente de Ollama inyectado por FastAPI.
    :type client: server.services.ollama.OllamaClient
    :param preferences: Descripción de lo que busca el usuario.
    :type preferences: str
    :returns: Recomendaciones generadas por el modelo.
    :rtype: server.schemas.responses.RecommendationResponse
    :raises fastapi.HTTPException: ``500`` si Ollama no responde.
    """
    prompt = (
        "You are an AI product recommender. Based on the user's preferences, "
        "suggest the best matching products.\n\n"
        f"User Preferences: {preferences}\n\n"
        "Recommended Products:\n"
    )
    recommendations = _generate_text(
        client,
        prompt,
        "No recommendations found.",
    )
    return RecommendationResponse(recommendations=recommendations)
