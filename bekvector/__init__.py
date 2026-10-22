"""
BekVector Engine — Procedural Vector Graphics & Animation Framework.
Developed by Bagas Cihuy (Bagas Saputra) with Bikagent.
"""

from .core import BekVector, Shapes, compute_damped_tangent, format_coord
from .animation import VectorAnimation
from .renderer import render_png, render_mp4

__version__ = "1.0.0"
__author__ = "Bagas Cihuy"
__all__ = [
    "BekVector",
    "Shapes",
    "VectorAnimation",
    "compute_damped_tangent",
    "format_coord",
    "render_png",
    "render_mp4"
]
