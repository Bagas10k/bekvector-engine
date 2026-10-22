"""
BekVector Engine — Procedural Vector Graphics & Animation Framework.
Developed by Bagas Cihuy (Bagas Saputra) with Bikagent.
"""

from .core import BekVector, Shapes, compute_damped_tangent, format_coord
from .animation import VectorAnimation
from .renderer import render_png, render_mp4
from .dataviz import DataViz
from .svg_animator import generate_animated_weather_svg
from .filters import get_grain_filter, get_gooey_filter, get_frosted_specular_filter
from .themes import get_theme, THEMES, Theme
from .spring import Spring
from .exporter import to_react_component, to_vue_component
from .studio import run_studio

__version__ = "1.2.0"
__author__ = "Bagas Cihuy"
__all__ = [
    "BekVector",
    "Shapes",
    "VectorAnimation",
    "DataViz",
    "Spring",
    "Theme",
    "THEMES",
    "get_theme",
    "generate_animated_weather_svg",
    "get_grain_filter",
    "get_gooey_filter",
    "get_frosted_specular_filter",
    "to_react_component",
    "to_vue_component",
    "run_studio",
    "compute_damped_tangent",
    "format_coord",
    "render_png",
    "render_mp4"
]
