"""
BekVector DataViz — High-Performance Procedural Chart & Telemetry Generator.
Generates lightweight, zero-dependency SVG sparklines, radar charts, and data bars.
"""

import math
from typing import List, Dict, Tuple
from .core import BekVector, format_coord

class DataViz:
    @staticmethod
    def sparkline(data: List[float], width: float = 240, height: float = 60, stroke: str = "#10B981", stroke_w: float = 2.5, fill_area: bool = True, fill_color: str = "rgba(16, 185, 129, 0.12)") -> str:
        """Generates a crisp, responsive SVG sparkline trend chart with area gradient."""
        if len(data) < 2:
            return ""

        min_val = min(data)
        max_val = max(data)
        val_range = max_val - min_val if max_val != min_val else 1.0

        pts: List[Tuple[float, float]] = []
        pad_x = 4.0
        pad_y = 6.0
        usable_w = width - (2 * pad_x)
        usable_h = height - (2 * pad_y)

        for i, val in enumerate(data):
            x = pad_x + (i / (len(data) - 1)) * usable_w
            # Invert y because SVG y=0 is top
            y = (height - pad_y) - ((val - min_val) / val_range) * usable_h
            pts.append((x, y))

        # Path string
        d_line = f"M{format_coord(pts[0][0])} {format_coord(pts[0][1])}"
        for p in pts[1:]:
            d_line += f"L{format_coord(p[0])} {format_coord(p[1])}"

        area_svg = ""
        if fill_area:
            d_area = f"{d_line} L{format_coord(pts[-1][0])} {height} L{format_coord(pts[0][0])} {height} Z"
            area_svg = f'<path d="{d_area}" fill="{fill_color}"/>'

        # Last point pulse indicator
        last_x, last_y = pts[-1]
        dot_svg = f'<circle cx="{format_coord(last_x)}" cy="{format_coord(last_y)}" r="3.5" fill="{stroke}" stroke="#FFFFFF" stroke-width="1.5"/>'

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  {area_svg}
  <path d="{d_line}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round"/>
  {dot_svg}
</svg>"""
        return svg

    @staticmethod
    def radar_chart(metrics: Dict[str, float], max_val: float = 100.0, radius: float = 100.0, stroke: str = "#FA5D29", fill: str = "rgba(250, 93, 41, 0.2)") -> str:
        """Generates an N-axis polar radar / spider chart with auto-padded axis labels."""
        keys = list(metrics.keys())
        n = len(keys)
        if n < 3:
            return ""

        cx, cy = radius + 60, radius + 60
        total_w = total_h = (radius + 60) * 2

        # Concentric grid rings
        rings_svg = []
        for level in [0.25, 0.5, 0.75, 1.0]:
            r_level = radius * level
            ring_pts = []
            for i in range(n):
                angle = (2 * math.pi / n) * i - (math.pi / 2)
                x = cx + r_level * math.cos(angle)
                y = cy + r_level * math.sin(angle)
                ring_pts.append(f"{format_coord(x)},{format_coord(y)}")
            rings_svg.append(f'<polygon points="{" ".join(ring_pts)}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>')

        # Axis spokes and labels
        spokes_svg = []
        labels_svg = []
        data_pts = []

        for i, (k, val) in enumerate(metrics.items()):
            angle = (2 * math.pi / n) * i - (math.pi / 2)
            # Spoke line
            spoke_x = cx + radius * math.cos(angle)
            spoke_y = cy + radius * math.sin(angle)
            spokes_svg.append(f'<line x1="{cx}" y1="{cy}" x2="{format_coord(spoke_x)}" y2="{format_coord(spoke_y)}" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>')

            # Label placement
            lbl_r = radius + 22
            lbl_x = cx + lbl_r * math.cos(angle)
            lbl_y = cy + lbl_r * math.sin(angle) + 4
            anchor = "middle"
            if math.cos(angle) > 0.3:
                anchor = "start"
            elif math.cos(angle) < -0.3:
                anchor = "end"
            labels_svg.append(f'<text x="{format_coord(lbl_x)}" y="{format_coord(lbl_y)}" fill="#8E9AA8" font-size="10" font-family="monospace" text-anchor="{anchor}">{k}</text>')

            # Data point
            norm_val = min(max_val, max(0.0, val)) / max_val
            dp_r = radius * norm_val
            d_x = cx + dp_r * math.cos(angle)
            d_y = cy + dp_r * math.sin(angle)
            data_pts.append(f"{format_coord(d_x)},{format_coord(d_y)}")

        # Data polygon
        poly_data = f'<polygon points="{" ".join(data_pts)}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">
  {"".join(rings_svg)}
  {"".join(spokes_svg)}
  {poly_data}
  {"".join(labels_svg)}
</svg>"""
        return svg
