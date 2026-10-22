#!/usr/bin/env python3
"""
Example: Bekbek Mascot Duck Vector.
Generates the iconic Bekbek procedural mascot duck in SVG and PNG.
"""

from bekvector import BekVector, render_png

def create_duck() -> BekVector:
    v = BekVector(min_padding=24)
    # Background halo ring
    v.circle(0, 0, 190, fill="rgba(255,255,255,0.02)", stroke="rgba(255,255,255,0.06)", stroke_w=1.5)

    # Water ripples
    v.path([(-130, 95), (-60, 90), (0, 98), (70, 92), (140, 95)], stroke="#49B3FC", stroke_w=3, smooth=0.4, closed=False)
    v.path([(-90, 115), (-20, 112), (40, 118), (100, 114)], stroke="rgba(73, 179, 252, 0.4)", stroke_w=2, smooth=0.4, closed=False)

    # Body spline
    body_pts = [
        (-90, 40), (-115, 20), (-80, 50), (-40, 85),
        (20, 88), (75, 70), (90, 40), (85, 10),
        (40, -10), (-10, 10), (-60, 25)
    ]
    v.path(body_pts, fill="#FFD166", stroke="#111111", stroke_w=3, smooth=0.35)

    # Head circle
    v.circle(42, -35, 48, fill="#FFD166", stroke="#111111", stroke_w=3)

    # Beak spline
    beak_pts = [(75, -28), (125, -22), (115, -10), (72, -12)]
    v.path(beak_pts, fill="#FA5D29", stroke="#111111", stroke_w=3, smooth=0.3)
    v.circle(88, -22, 2.5, fill="#8E2800")

    # Eye with specular catchlights
    v.circle(52, -45, 11, fill="#111111")
    v.circle(55, -48, 4, fill="#FFFFFF")
    v.circle(49, -42, 1.8, fill="#FFFFFF")

    # Blush
    v.ellipse(36, -26, 8, 5, fill="rgba(250, 93, 41, 0.25)")

    # Wing spline
    wing_pts = [(-50, 45), (-10, 32), (30, 45), (15, 68), (-25, 70)]
    v.path(wing_pts, fill="#FFC043", stroke="#111111", stroke_w=2.5, smooth=0.4)

    # Droplets
    v.circle(-105, 75, 4, fill="#49B3FC")
    v.circle(115, 80, 5, fill="#49B3FC")

    # Captions
    v.text(0, 155, "BEKBEK — PROCEDURAL DUCK", font_size=12, fill="#EDEDED", letter_spacing=2.5)
    v.text(0, 172, "100% SVG CODE · ZERO PIXELS", font_size=9, fill="#FA5D29", letter_spacing=1.8)

    return v

if __name__ == "__main__":
    duck = create_duck()
    svg = duck.to_svg(bg="#0B0D13")
    with open("assets/bekbek_duck.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    render_png(svg, "assets/bekbek_duck.png")
    print("Rendered assets/bekbek_duck.svg & assets/bekbek_duck.png")
