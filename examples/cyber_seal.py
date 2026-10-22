#!/usr/bin/env python3
"""
Example: Cybernetic Insignia / System Seal.
Generates an authoritative, dark-mode technical seal in SVG and PNG.
"""

import math
from bekvector import BekVector, render_png

def create_seal() -> BekVector:
    v = BekVector(min_padding=24)
    # Outer geometric rings
    v.circle(0, 0, 180, fill="none", stroke="#222630", stroke_w=2)
    v.circle(0, 0, 160, fill="rgba(255,255,255,0.02)", stroke="#FA5D29", stroke_w=1.5)

    # Radiating ticks
    for i in range(36):
        ang = math.radians(i * 10)
        r1 = 168 if i % 3 == 0 else 164
        r2 = 175
        x1, y1 = r1 * math.cos(ang), r1 * math.sin(ang)
        x2, y2 = r2 * math.cos(ang), r2 * math.sin(ang)
        v.path([(x1, y1), (x2, y2)], stroke="#4A5263" if i % 3 != 0 else "#FA5D29", stroke_w=1.5, smooth=0, closed=False)

    # Core frosted diamond
    v.rect(0, 0, 140, 140, fill="rgba(25, 28, 36, 0.8)", stroke="#49B3FC", stroke_w=1.5, r=16, rot=45)
    v.rect(0, 0, 100, 100, fill="rgba(250, 93, 41, 0.08)", stroke="rgba(255,255,255,0.15)", stroke_w=1, r=8, rot=45)

    # Dynamic spline wave
    wave_pts = []
    for step in range(9):
        wx = -90 + step * 22.5
        wy = math.sin(step * 0.8) * 25
        wave_pts.append((wx, wy))
    v.path(wave_pts, stroke="#49B3FC", stroke_w=3, smooth=0.4, closed=False)

    # Core node
    v.circle(0, 0, 18, fill="#FA5D29", stroke="#FFFFFF", stroke_w=2)
    v.circle(0, 0, 6, fill="#FFFFFF")

    # Typography anchors
    v.text(0, -60, "AUTONOMOUS SYSTEM", font_size=11, fill="#8E9AA8", letter_spacing=2)
    v.text(0, 75, "VERIFIED PROTOCOL", font_size=10, fill="#FA5D29", letter_spacing=2.5)

    return v

if __name__ == "__main__":
    seal = create_seal()
    svg = seal.to_svg(bg="#0A0B0E")
    with open("assets/cyber_seal.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    render_png(svg, "assets/cyber_seal.png")
    print("Rendered assets/cyber_seal.svg & assets/cyber_seal.png")
