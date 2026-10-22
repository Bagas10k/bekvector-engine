"""
BekVector Core Engine — Pure Mathematical Vector Generation.
Constructs smooth Catmull-Rom splines, geometric primitives, and auto-computed viewboxes.
"""

import math
from typing import List, Tuple, Optional

def compute_damped_tangent(p_prev: Tuple[float, float], p_curr: Tuple[float, float], p_next: Tuple[float, float], base_smooth: float = 0.35) -> Tuple[float, float]:
    """Computes Catmull-Rom tangent with acute angle damping to prevent loop overshoot."""
    v1 = (p_curr[0] - p_prev[0], p_curr[1] - p_prev[1])
    v2 = (p_next[0] - p_curr[0], p_next[1] - p_curr[1])

    d1 = math.hypot(*v1)
    d2 = math.hypot(*v2)

    if d1 < 1e-4 or d2 < 1e-4:
        return (0.0, 0.0)

    cos_theta = (v1[0] * v2[0] + v1[1] * v2[1]) / (d1 * d2)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    turn_angle = math.acos(cos_theta)

    damping = 1.0 - (turn_angle / math.pi) * 0.65
    effective_smooth = base_smooth * max(0.2, damping)

    tx = (p_next[0] - p_prev[0]) * effective_smooth / 2.0
    ty = (p_next[1] - p_prev[1]) * effective_smooth / 2.0

    return (tx, ty)

def format_coord(val: float) -> str:
    """Formats coordinate to 1 decimal place, stripping trailing zeros for 70%+ token efficiency."""
    rounded = round(val, 1)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.1f}"

class BekVector:
    """Procedural vector canvas building resolution-independent SVG elements."""
    def __init__(self, min_padding: float = 12):
        self.items: List[str] = []
        self.minx: float = float('inf')
        self.miny: float = float('inf')
        self.maxx: float = float('-inf')
        self.maxy: float = float('-inf')
        self.max_stroke: float = 0.0
        self.min_padding: float = min_padding

    def _box(self, pts: List[Tuple[float, float]], stroke_w: float = 0.0):
        self.max_stroke = max(self.max_stroke, stroke_w)
        for x, y in pts:
            self.minx = min(self.minx, x)
            self.miny = min(self.miny, y)
            self.maxx = max(self.maxx, x)
            self.maxy = max(self.maxy, y)

    def rect(self, x: float, y: float, w: float, h: float, fill: str = "none", stroke: str = "none", stroke_w: float = 1.0, r: float = 0.0, rot: float = 0.0):
        """Draws a centered rectangle with corner radius and rotation."""
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        self._box([(x + dx * ca - dy * sa, y + dx * sa + dy * ca)
                   for dx in (-w/2, w/2) for dy in (-h/2, h/2)], stroke_w)
        style = f'fill="{fill}"'
        if stroke != "none":
            style += f' stroke="{stroke}" stroke-width="{stroke_w}"'
        self.items.append(
            f'<rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" '
            f'{style} transform="translate({x:.1f} {y:.1f}) rotate({rot})"/>'
        )
        return self

    rc = rect  # alias

    def ellipse(self, x: float, y: float, rx: float, ry: float, fill: str = "none", stroke: str = "none", stroke_w: float = 1.0):
        """Draws an ellipse at (x, y)."""
        self._box([(x - rx, y - ry), (x + rx, y + ry)], stroke_w)
        style = f'fill="{fill}"'
        if stroke != "none":
            style += f' stroke="{stroke}" stroke-width="{stroke_w}"'
        self.items.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" {style}/>')
        return self

    el = ellipse  # alias

    def circle(self, x: float, y: float, r: float, fill: str = "none", stroke: str = "none", stroke_w: float = 1.0):
        """Draws a circle at (x, y)."""
        return self.ellipse(x, y, r, r, fill, stroke, stroke_w)

    def path(self, pts: List[Tuple[float, float]], fill: str = "none", stroke: str = "none", stroke_w: float = 1.0, smooth: float = 0.35, closed: bool = True):
        """Constructs an organic Catmull-Rom spline converted to cubic Bezier commands."""
        if not pts:
            return self
        n = len(pts)
        if n < 3 or smooth == 0:
            d = f'M{format_coord(pts[0][0])} {format_coord(pts[0][1])}'
            for p in pts[1:]:
                d += f'L{format_coord(p[0])} {format_coord(p[1])}'
            if closed:
                d += 'Z'
            self._box(pts, stroke_w)
        else:
            t_vec = []
            for k in range(n):
                prev_p, next_p = pts[(k - 1) % n], pts[(k + 1) % n]
                t_vec.append(compute_damped_tangent(prev_p, pts[k], next_p, smooth))

            d = f'M{format_coord(pts[0][0])} {format_coord(pts[0][1])}'
            for k in range(n):
                p0, p1 = pts[k], pts[(k + 1) % n]
                c1 = (p0[0] + t_vec[k][0], p0[1] + t_vec[k][1])
                c2 = (p1[0] - t_vec[(k + 1) % n][0], p1[1] - t_vec[(k + 1) % n][1])
                d += f'C{format_coord(c1[0])} {format_coord(c1[1])} {format_coord(c2[0])} {format_coord(c2[1])} {format_coord(p1[0])} {format_coord(p1[1])}'
                self._box([c1, c2, p1], stroke_w)
            if closed:
                d += 'Z'

        style = f'fill="{fill}"'
        if stroke != "none":
            style += f' stroke="{stroke}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round"'
        self.items.append(f'<path d="{d}" {style}/>')
        return self

    pth = path  # alias

    def text(self, x: float, y: float, content: str, font_size: float = 12.0, fill: str = "#EDEDED", font_family: str = "Inter Tight, monospace", letter_spacing: float = 1.0, text_anchor: str = "middle"):
        """Draws architectural text labels."""
        self._box([(x - 80, y - font_size), (x + 80, y + font_size)])
        self.items.append(
            f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{font_size}" font-family="{font_family}" '
            f'letter-spacing="{letter_spacing}" text-anchor="{text_anchor}">{content}</text>'
        )
        return self

    def to_svg(self, bg: Optional[str] = "#0A0B0E") -> str:
        """Compiles geometry into a standalone, valid SVG document with stroke dilation compensation."""
        stroke_bleed = math.ceil(self.max_stroke / 2.0)
        pad = max(self.min_padding, stroke_bleed + 6)
        x0 = math.floor(self.minx - pad)
        y0 = math.floor(self.miny - pad)
        w = math.ceil(self.maxx + pad) - x0
        h = math.ceil(self.maxy + pad) - y0
        bg_rect = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">{bg_rect}{"".join(self.items)}</svg>'

# Backward-compatible alias
Shapes = BekVector
