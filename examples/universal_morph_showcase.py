import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(HERE)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from bekvector import UniversalMorph, render_mp4
from bekvector.universal_morph import TransitionVelocity
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

def render_velocity_video():
    frame_dir = "/tmp/universal_morph_velocity_frames"
    os.makedirs(frame_dir, exist_ok=True)
    total_frames = 180 # 3.0s @ 60 FPS
    fps = 60

    print(f"Rendering {total_frames} velocity-tuned morph frames @ {fps} FPS...")
    pairs = [
        ("heart", "star", "#FF4D6D", "#FFD000", "Favorit ➔ Rating"),
        ("shield", "gear", "#49B3FC", "#A0C4FF", "Security ➔ Settings"),
        ("bell", "bolt", "#FA5D29", "#FFD000", "Alert ➔ Quick Action"),
        ("cloud", "search", "#34D399", "#49B3FC", "Cloud Storage ➔ Query"),
    ]

    for f in range(total_frames):
        p = f / total_frames # 0.0 to 1.0

        # Cycle breakdown:
        # 0.00 - 0.15: Hold at Shape A (Pause to read)
        # 0.15 - 0.45: SNAPPY SPRING MORPH from A -> B (Rapid velocity burst + bounce)
        # 0.45 - 0.65: Hold at Shape B (Pause to read)
        # 0.65 - 0.95: SNAPPY SPRING MORPH from B -> A (Rapid velocity burst + bounce)
        # 0.95 - 1.00: Settle at Shape A
        
        if p < 0.15:
            morph_val = 0.0
            scale_mod = 1.0
        elif p < 0.45:
            sub_t = (p - 0.15) / 0.30
            morph_val = TransitionVelocity.snappy_spring(sub_t, overshoot=0.08, damping=14)
            vel_intensity = math.sin(sub_t * math.pi)
            scale_mod = 1.0 - vel_intensity * 0.06
        elif p < 0.65:
            morph_val = 1.0
            scale_mod = 1.0
        elif p < 0.95:
            sub_t = (p - 0.65) / 0.30
            morph_forward = TransitionVelocity.snappy_spring(sub_t, overshoot=0.08, damping=14)
            morph_val = 1.0 - morph_forward
            vel_intensity = math.sin(sub_t * math.pi)
            scale_mod = 1.0 - vel_intensity * 0.06
        else:
            morph_val = 0.0
            scale_mod = 1.0

        cards = []
        for i, (icon_a, icon_b, col_a, col_b, label) in enumerate(pairs):
            cx = 40 + i * 285
            cy = 75

            clamped_val = max(0.0, min(1.0, morph_val))
            path_d = UniversalMorph.morph_between(icon_a, icon_b, clamped_val, num_samples=72)
            fill_col = col_b if clamped_val > 0.5 else col_a

            cards.append(f"""
    <g transform="translate({cx}, {cy})">
      <rect width="260" height="260" rx="20" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
      <line x1="20" y1="200" x2="240" y2="200" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1" />
      <g transform="translate(130, 105) scale({1.6 * scale_mod:.3f}) translate(-32, -32)">
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
    BEKVISUAL · DYNAMIC TRANSITION VELOCITY
  </text>
  <text x="1160" y="44" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#FA5D29" text-anchor="end">
    SNAPPY ACCELERATION + SPRING OVERSHOOT (60 FPS)
  </text>
  <line x1="40" y1="56" x2="1160" y2="56" stroke="rgba(255,255,255,0.12)" stroke-width="1.2" />
  {''.join(cards)}
</svg>"""

        png_data = resvg_py.svg_to_bytes(frame_svg)
        frame_file = os.path.join(frame_dir, f"frame_{f:03d}.png")
        with open(frame_file, "wb") as f_out:
            f_out.write(png_data)

    out_mp4 = os.path.join(ROOT_DIR, "assets", "universal_morphs_velocity.mp4")
    render_mp4(frame_dir, out_mp4, fps=fps)
    print(f"Generated 60 FPS Velocity-Tuned Video MP4: {out_mp4}")
    return out_mp4

if __name__ == "__main__":
    generate_svg_and_png()
    render_velocity_video()
