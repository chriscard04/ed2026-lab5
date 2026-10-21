"""labkit · caja de herramientas del Lab 5 de Estructura de Datos (UTP · ED2026)."""

from .algoritmos import camino, recorrer
from .cliente import ErrorLab, Lab
from .fronteras import CustomCola, CustomPila, FronteraHeap, nombre_frontera

__version__ = "1.0.0"
__all__ = ["Lab", "ErrorLab", "CustomPila", "CustomCola", "FronteraHeap", "nombre_frontera", "recorrer", "camino"]
