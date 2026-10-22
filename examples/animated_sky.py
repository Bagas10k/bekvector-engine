#!/usr/bin/env python3
"""
Example: Procedural Animated Vector Sky Loop.
Generates an atmospheric night sky with floating moon, twinkling stars, shooting star,
and parallax multi-layer clouds compiled into an MP4 video.
"""

import math
from bekvector import BekVector
from bekvector.animation import VectorAnimation

def generate_sky_frame(t_norm: float) -> str:
    W, H = 720, 480
    moon_x = 540 + math.sin(t_norm * 2 * math.pi) * 4
    moon_y = 110 + math.cos(t_norm * 2 * math.pi) * 3

    stars = []
    star_defs = [
        (80, 70, 2.5, 0.0), (160, 110, 1.8, 0.25), (240, 60, 2.0, 0.5),
        (320, 130, 1.5, 0.75), (410, 80, 2.8, 0.1), (490, 50, 1.5, 0.4),
        (620, 95, 2.2, 0.6), (120, 180, 1.5, 0.8), (280, 210, 1.8, 0.3),
        (460, 170, 2.0, 0.9), (650, 160, 1.5, 0.15), (70, 130, 2.0, 0.7)
    ]
    for sx, sy, sr, phase in star_defs:
        twinkle = 0.3 + 0.7 * (0.5 + 0.5 * math.sin((t_norm + phase) * 2 * math.pi))
        stars.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*twinkle:.2f}" fill="#FFFFFF" opacity="{twinkle:.2f}"/>')

    shooting_star = ""
    if 0.3 <= t_norm <= 0.65:
        st_progress = (t_norm - 0.3) / 0.35
        st_x1 = 380 - st_progress * 160
        st_y1 = 40 + st_progress * 90
        st_x2 = st_x1 + 35
        st_y2 = st_y1 - 20
        st_opacity = math.sin(st_progress * math.pi) * 0.9
        shooting_star = f'<line x1="{st_x1:.1f}" y1="{st_y1:.1f}" x2="{st_x2:.1f}" y2="{st_y2:.1f}" stroke="#FA5D29" stroke-width="2" stroke-linecap="round" opacity="{st_opacity:.2f}"/>'

    cloud1_offset = (t_norm * 180) % W
    def cloud_shape(offset_x, base_y, scale_w, scale_h, color):
        shapes = []
        for shift in [-W, 0, W]:
            cx = offset_x + shift
            shapes.append(f'<path d="M {cx-120*scale_w:.1f} {base_y} '
                          f'Q {cx-80*scale_w:.1f} {base_y-40*scale_h:.1f} {cx-40*scale_w:.1f} {base_y-25*scale_h:.1f} '
                          f'Q {cx:.1f} {base_y-65*scale_h:.1f} {cx+50*scale_w:.1f} {base_y-30*scale_h:.1f} '
                          f'Q {cx+100*scale_w:.1f} {base_y-45*scale_h:.1f} {cx+130*scale_w:.1f} {base_y} Z" fill="{color}"/>')
        return "".join(shapes)

    c1 = cloud_shape(cloud1_offset + 100, 220, 1.2, 0.9, "rgba(45, 52, 75, 0.45)")
    c2 = cloud_shape(cloud1_offset + 420, 250, 1.4, 0.8, "rgba(45, 52, 75, 0.45)")

    cloud2_offset = (t_norm * 260) % W
    c3 = cloud_shape(cloud2_offset + 250, 310, 1.5, 1.1, "rgba(28, 33, 50, 0.75)")
    c4 = cloud_shape(cloud2_offset - 50, 330, 1.6, 1.0, "rgba(28, 33, 50, 0.75)")

    mountain_pts = [
        (-40, H), (0, 390), (90, 420), (180, 370), (270, 410),
        (380, 350), (480, 395), (580, 360), (670, 400), (W+40, 380), (W+40, H)
    ]
    mtn_d = "M " + " L ".join([f"{x} {y}" for x, y in mountain_pts]) + " Z"

    cloud3_offset = (t_norm * 340) % W
    c5 = cloud_shape(cloud3_offset + 80, 420, 1.8, 1.2, "rgba(15, 17, 26, 0.95)")
    c6 = cloud_shape(cloud3_offset + 480, 430, 1.9, 1.3, "rgba(15, 17, 26, 0.95)")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#08090E"/>
      <stop offset="40%" stop-color="#111625"/>
      <stop offset="75%" stop-color="#22213A"/>
      <stop offset="100%" stop-color="#422438"/>
    </linearGradient>
    <radialGradient id="moonHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgba(255, 235, 180, 0.35)"/>
      <stop offset="100%" stop-color="rgba(255, 235, 180, 0)"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#skyGrad)"/>
  {''.join(stars)}
  {shooting_star}
  <circle cx="{moon_x:.1f}" cy="{moon_y:.1f}" r="42" fill="url(#moonHalo)"/>
  <circle cx="{moon_x:.1f}" cy="{moon_y:.1f}" r="24" fill="#FFE8A3"/>
  <circle cx="{moon_x-9:.1f}" cy="{moon_y-7:.1f}" r="22" fill="#111625"/>
  {c1}{c2}{c3}{c4}
  <path d="{mtn_d}" fill="#0D0F17" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  {c5}{c6}
  <rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1" rx="16"/>
  <text x="28" y="450" fill="#8E9AA8" font-family="monospace" font-size="10" letter-spacing="2">PROCEDURAL VECTOR SKY · 60 FPS MORPH</text>
  <text x="{W-28}" y="450" fill="#FA5D29" font-family="monospace" font-size="10" letter-spacing="2" text-anchor="end">LIVE ENGINE</text>
</svg>"""

if __name__ == "__main__":
    anim = VectorAnimation(generate_sky_frame, total_frames=90, fps=30)
    out_mp4 = anim.export_mp4("assets/vektor_langit.mp4")
    print(f"Generated animation loop: {out_mp4}")
