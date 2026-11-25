"""Catálogo de productos de ejemplo del recomendador.

.. note::
   La versión original construía un ``DataFrame`` de pandas que nunca se
   utilizaba. El catálogo se conserva aquí como referencia, pero **no se
   envía al modelo**: el prompt solo incluye las preferencias del usuario.
"""
from typing import TypedDict


class Product(TypedDict):
    """Producto del catálogo de ejemplo.

    :ivar id: Identificador numérico.
    :ivar category: Categoría comercial del producto.
    :ivar name: Nombre visible del producto.
    """

    id: int
    category: str
    name: str


PRODUCTS: list[Product] = [
    {"id": 1, "category": "Electronics", "name": "Wireless Earbuds"},
    {"id": 2, "category": "Electronics", "name": "Smartphone"},
    {"id": 3, "category": "Electronics", "name": "Laptop"},
    {"id": 4, "category": "Fashion", "name": "Leather Jacket"},
    {"id": 5, "category": "Fashion", "name": "Running Shoes"},
    {"id": 6, "category": "Home", "name": "Smart Vacuum Cleaner"},
    {"id": 7, "category": "Home", "name": "Air Purifier"},
]
