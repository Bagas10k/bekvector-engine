import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(HERE)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from bekvector import UniversalMorph, render_mp4
import resvg_py

def generate_svg_and_png():
    svg_code = UniversalMorph.generate_universal_stage(width=1200, height=380)
    out_svg = os.path.join(ROOT_DIR, "assets", "universal_morphs.svg")
    out_png = os.path.join(ROOT_DIR, "assets", "universal_morphs.png")

    os.makedirs(os.path.dirname(out_svg), exist_ok=True)
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_code)

    png_bytes = resvg_py.svg_to_bytes(svg_code)
    with open(out_png, "wb") as f:
        f.write(png_bytes)

    print(f"Generated {out_svg} & {out_png}")
    return out_svg, out_png

def render_video():
    frame_dir = "/tmp/universal_morph_frames"
    os.makedirs(frame_dir, exist_ok=True)
    total_frames = 180 # 3 seconds @ 60 FPS
    fps = 60

    print(f"Rendering {total_frames} universal morph frames @ {fps} FPS...")
    pairs = [
        ("heart", "star", "#FF4D6D", "#FFD000", "Favorit ➔ Rating"),
        ("shield", "gear", "#49B3FC", "#A0C4FF", "Security ➔ Settings"),
        ("bell", "bolt", "#FA5D29", "#FFD000", "Alert ➔ Quick Action"),
        ("cloud", "search", "#34D399", "#49B3FC", "Cloud Storage ➔ Query"),
    ]

    for f in range(total_frames):
        p = f / total_frames
        # Cosine ping-pong easing
        ease = (1.0 - math.cos(p * 2 * math.pi)) / 2.0

        cards = []
        for i, (icon_a, icon_b, col_a, col_b, label) in enumerate(pairs):
            cx = 40 + i * 285
            cy = 75

            # Interpolate path at current ease
            path_d = UniversalMorph.morph_between(icon_a, icon_b, ease, num_samples=72)
            
            # Simple color blend
            fill_col = col_b if ease > 0.5 else col_a

            cards.append(f"""
    <g transform="translate({cx}, {cy})">
      <rect width="260" height="260" rx="20" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
      <line x1="20" y1="200" x2="240" y2="200" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1" />
      <g transform="translate(130, 105) scale(1.6) translate(-32, -32)">
        <path d="{path_d}" fill="{fill_col}" opacity="0.95" />
      </g>
      <text x="130" y="224" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700" fill="#EDEDED" text-anchor="middle" letter-spacing="0.08em">
        {icon_a.upper()} ➔ {icon_b.upper()}
      </text>
      <text x="130" y="242" font-family="'Inter', sans-serif" font-size="10.5" font-weight="500" fill="#8892B0" text-anchor="middle">
        {label}
      </text>
    </g>
""")

        frame_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380">
  <defs>
    <linearGradient id="universalBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#08090C" />
      <stop offset="50%" stop-color="#121622" />
      <stop offset="100%" stop-color="#08090C" />
    </linearGradient>
  </defs>
  <rect width="1200" height="380" fill="url(#universalBg)" />
  <text x="40" y="44" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="#EDEDED" letter-spacing="0.04em">
    BEKVISUAL · UNIVERSAL ICON MORPHING ENGINE
  </text>
  <text x="1160" y="44" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#FA5D29" text-anchor="end">
    ARCLENGTH RESAMPLING &amp; ROTATION ALIGNED (ANY SHAPE ➔ ANY SHAPE)
  </text>
  <line x1="40" y1="56" x2="1160" y2="56" stroke="rgba(255,255,255,0.12)" stroke-width="1.2" />
  {''.join(cards)}
</svg>"""

        png_data = resvg_py.svg_to_bytes(frame_svg)
        frame_file = os.path.join(frame_dir, f"frame_{f:03d}.png")
        with open(frame_file, "wb") as f_out:
            f_out.write(png_data)

    out_mp4 = os.path.join(ROOT_DIR, "assets", "universal_morphs.mp4")
    render_mp4(frame_dir, out_mp4, fps=fps)
    print(f"Generated 60 FPS Universal Morph Video MP4: {out_mp4}")
    return out_mp4

if __name__ == "__main__":
    generate_svg_and_png()
    render_video()
