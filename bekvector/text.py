"""
BekVector Text-to-Path — Converts Text Strings into Mathematical SVG Vector Shapes.
Extracts font glyph outlines via fontTools and compiles them into animatable <path> elements.
"""

import os
from typing import List, Dict, Optional, Tuple

DEFAULT_FONTS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]

def find_default_font() -> str:
    for f in DEFAULT_FONTS:
        if os.path.exists(f):
            return f
    return ""

class TextToPath:
    @staticmethod
    def convert(
        text: str,
        font_size: float = 64.0,
        font_path: Optional[str] = None,
        fill: str = "#EDEDED",
        stroke: str = "none",
        stroke_w: float = 1.0,
        letter_spacing: float = 0.0,
        x_offset: float = 0.0,
        y_offset: float = 0.0
    ) -> Dict:
        """Converts a text string into mathematical SVG glyph vector paths."""
        from fontTools.ttLib import TTFont
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen

        font_file = font_path or find_default_font()
        if not font_file or not os.path.exists(font_file):
            raise FileNotFoundError("No valid TTF font found on system for Text-to-Path conversion.")

        font = TTFont(font_file)
        glyph_set = font.getGlyphSet()
        cmap = font.getBestCmap()

        units_per_em = font['head'].unitsPerEm
        scale = font_size / units_per_em

        current_x = x_offset
        baseline_y = y_offset + font_size
        glyphs = []

        for idx, char in enumerate(text):
            if char == " ":
                current_x += (font_size * 0.3) + letter_spacing
                continue

            if ord(char) not in cmap:
                continue

            glyph_name = cmap[ord(char)]
            glyph = glyph_set[glyph_name]

            char_pen = SVGPathPen(glyph_set)
            # Transform font bottom-up coordinates to SVG top-down coordinates
            tpen = TransformPen(char_pen, (scale, 0, 0, -scale, current_x, baseline_y))
            glyph.draw(tpen)
            d = char_pen.getCommands()

            advance_w = (glyph.width * scale) + letter_spacing
            if d:
                glyphs.append({
                    "char": char,
                    "index": idx,
                    "d": d,
                    "x": current_x,
                    "width": advance_w,
                    "svg_path": f'<path id="glyph-{idx}" class="text-glyph glyph-{idx}" d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
                })
            current_x += advance_w

        total_width = current_x - x_offset
        total_height = font_size * 1.35

        return {
            "text": text,
            "font_size": font_size,
            "width": total_width,
            "height": total_height,
            "glyphs": glyphs,
            "combined_paths": "".join([g["svg_path"] for g in glyphs])
        }

    @staticmethod
    def create_animated_text_svg(
        text: str,
        font_size: float = 64.0,
        fill: str = "#EDEDED",
        accent_color: str = "#FA5D29",
        accent_indices: Optional[List[int]] = None,
        animation_type: str = "stagger_rise",
        bg: str = "#0A0B0E"
    ) -> str:
        """Generates an animated standalone SVG where each text letter animates individually."""
        data = TextToPath.convert(text, font_size=font_size, x_offset=24, y_offset=16)
        w = int(data["width"] + 48)
        h = int(data["height"] + 32)
        accents = accent_indices or []

        styled_paths = []
        for g in data["glyphs"]:
            idx = g["index"]
            char_fill = accent_color if idx in accents else fill
            styled_paths.append(
                f'<path id="glyph-{idx}" class="text-glyph glyph-{idx}" d="{g["d"]}" '
                f'fill="{char_fill}" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
            )

        if animation_type == "stagger_rise":
            keyframes = """
      @keyframes letterRise {
        0% { transform: translateY(24px) scale(0.85); opacity: 0; }
        100% { transform: translateY(0) scale(1.0); opacity: 1; }
      }
      .text-glyph {
        animation: letterRise 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
"""
            # Inject stagger delays
            stagger_css = "".join([f"      .glyph-{g['index']} {{ animation-delay: {g['index'] * 0.06:.2f}s; }}\n" for g in data["glyphs"]])
        elif animation_type == "stroke_draw":
            keyframes = """
      @keyframes drawStroke {
        0% { stroke-dashoffset: 600; fill-opacity: 0; }
        70% { stroke-dashoffset: 0; fill-opacity: 0.2; }
        100% { stroke-dashoffset: 0; fill-opacity: 1; }
      }
      .text-glyph {
        stroke: #FA5D29;
        stroke-width: 2;
        stroke-dasharray: 600;
        animation: drawStroke 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
"""
            stagger_css = "".join([f"      .glyph-{g['index']} {{ animation-delay: {g['index'] * 0.12:.2f}s; }}\n" for g in data["glyphs"]])
        else:
            keyframes = ""
            stagger_css = ""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
{keyframes}
{stagger_css}
    </style>
  </defs>
  <rect width="{w}" height="{h}" rx="16" fill="{bg}" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  {"".join(styled_paths)}
</svg>"""
        return svg
