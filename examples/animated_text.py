#!/usr/bin/env python3
"""
Example: Text-to-Path Vector Conversion & Kinetic Animation.
Converts any text string into mathematical SVG glyph vector paths and animates them.
"""

import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(HERE)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from bekvector import BekVector, render_png
from bekvector.text import TextToPath
from bekvector.animation import VectorAnimation

def generate_text_frame(t_norm: float, text: str = "BEKVEKTOR") -> str:
    """Generates a kinetic frame of text vectors with spring bounce and stroke drawing."""
    data = TextToPath.convert(text, font_size=72, x_offset=30, y_offset=25)
    w = int(data["width"] + 60)
    h = int(data["height"] + 50)

    paths = []
    total_chars = len(data["glyphs"])

    for i, g in enumerate(data["glyphs"]):
        # Staggered wave bounce per character
        char_phase = (i / total_chars)
        bounce_y = math.sin((t_norm * 2 * math.pi) + (char_phase * 2 * math.pi)) * 8
        scale = 1.0 + math.sin((t_norm * 2 * math.pi) + (char_phase * 2 * math.pi)) * 0.05

        # Color: First 3 letters Ember orange, rest Crisp white
        col = "#FA5D29" if i < 3 else "#EDEDED"

        # Transform per character
        cx = g["x"] + g["width"] / 2
        cy = data["height"] / 2
        transform = f'transform="translate(0, {bounce_y:.1f})"'

        paths.append(
            f'<path id="glyph-{i}" d="{g["d"]}" fill="{col}" stroke="#111111" stroke-width="2" {transform}/>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" rx="16" fill="#0A0B0E" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  {"".join(paths)}
</svg>"""
    return svg

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    # 1. Generate standalone pure CSS animated SVG
    svg_css = TextToPath.create_animated_text_svg("BEKVEKTOR", font_size=72, accent_color="#FA5D29", accent_indices=[0, 1, 2], animation_type="stagger_rise")
    with open("assets/bekvector_text_animated.svg", "w", encoding="utf-8") as f:
        f.write(svg_css)
    render_png(svg_css, "assets/bekvector_text.png")
    print("Generated assets/bekvector_text_animated.svg & assets/bekvector_text.png")

    # 2. Render MP4 animation loop
    anim = VectorAnimation(generate_text_frame, total_frames=60, fps=30)
    out_mp4 = anim.export_mp4("assets/bekvector_text_anim.mp4")
    print(f"Generated text animation MP4: {out_mp4}")
