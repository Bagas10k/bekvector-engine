import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(HERE)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from bekvector import IconMorph, render_png, render_mp4
import resvg_py

def generate_svg_and_png():
    svg_code = IconMorph.generate_showcase_stage(1000, 420)
    out_svg = os.path.join(ROOT_DIR, "assets", "ui_icon_morphs.svg")
    out_png = os.path.join(ROOT_DIR, "assets", "ui_icon_morphs.png")

    os.makedirs(os.path.dirname(out_svg), exist_ok=True)
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_code)

    png_bytes = resvg_py.svg_to_bytes(svg_code)
    with open(out_png, "wb") as f:
        f.write(png_bytes)

    print(f"Generated {out_svg} & {out_png}")
    return out_svg, out_png

def render_morph_video_frames():
    """
    Renders 180 frames (3 seconds @ 60 FPS) of mathematical morphing icons.
    """
    frame_dir = "/tmp/morph_frames"
    os.makedirs(frame_dir, exist_ok=True)
    total_frames = 180
    fps = 60

    print(f"Rendering {total_frames} morphing frames @ {fps} FPS...")
    for f in range(total_frames):
        t = f / fps # 0.0 to 3.0s
        p = (t % 3.0) / 3.0 # normalized 0 to 1
        
        # Smooth ping-pong progress via cosine easing (0 -> 1 -> 0)
        ease = (1.0 - math.cos(p * 2 * math.pi)) / 2.0

        # Morph 1: Hamburger -> Close X
        # Bar 1 rotates 0 to 45 deg, translateY 0 to 12
        r1 = ease * 45.0
        y1 = -12 + ease * 12.0
        r3 = -ease * 45.0
        y3 = 12 - ease * 12.0
        mid_scale = 1.0 - ease
        mid_opac = max(0.0, 1.0 - ease * 2.0)

        # Morph 2: Sun -> Moon
        # Sun rays fade out, center scoop moves in
        ray_scale = max(0.0, 1.0 - ease * 1.5)
        ray_rot = ease * 120.0
        moon_rot = ease * 160.0
        # Color transition from gold #FFD000 to blue-white #A0C4FF
        scoop_x = 40.0 - ease * 32.0
        scoop_y = -40.0 + ease * 32.0

        # Morph 3: Play -> Pause
        # Triangle transforms into 2 vertical bars
        bar_w = 4 + (1.0 - ease) * 4
        bar_gap = 6 + ease * 8

        # Morph 4: Download -> Checkmark
        # Ring spins, arrow condenses, check reveals
        ring_rot = ease * 720.0
        arrow_y = -ease * 15.0
        arrow_opac = max(0.0, 1.0 - ease * 2.2)
        check_dash = 35 * (1.0 - min(1.0, max(0.0, (ease - 0.4) * 2.5)))

        frame_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 420" width="1000" height="420">
  <defs>
    <linearGradient id="stageBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0D13" />
      <stop offset="50%" stop-color="#141824" />
      <stop offset="100%" stop-color="#08090C" />
    </linearGradient>
    <mask id="moon-mask-{f}">
      <rect x="-50" y="-50" width="100" height="100" fill="#FFFFFF" />
      <circle cx="{scoop_x:.1f}" cy="{scoop_y:.1f}" r="17" fill="#000000" />
    </mask>
  </defs>

  <rect width="1000" height="420" fill="url(#stageBg)" />

  <!-- Header -->
  <text x="40" y="44" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="#EDEDED" letter-spacing="0.04em">
    BEKVISUAL · DYNAMIC UI ICON MORPHING
  </text>
  <text x="960" y="44" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#FA5D29" text-anchor="end">
    60 FPS IN-PLACE FLUID TRANSFORMATION
  </text>
  <line x1="40" y1="56" x2="960" y2="56" stroke="rgba(255,255,255,0.1)" stroke-width="1.2" />

  <!-- CARD 1: HAMBURGER ➔ CLOSE -->
  <g transform="translate(40, 80)">
    <rect width="215" height="280" rx="18" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
    <g transform="translate(107, 105)">
      <line x1="-16" y1="0" x2="16" y2="0" stroke="#EDEDED" stroke-width="4" stroke-linecap="round" transform="translate(0, {y1:.1f}) rotate({r1:.1f})" />
      <line x1="-16" y1="0" x2="16" y2="0" stroke="#FA5D29" stroke-width="4" stroke-linecap="round" transform="scale({mid_scale:.2f}, 1)" opacity="{mid_opac:.2f}" />
      <line x1="-16" y1="0" x2="16" y2="0" stroke="#EDEDED" stroke-width="4" stroke-linecap="round" transform="translate(0, {y3:.1f}) rotate({r3:.1f})" />
    </g>
    <text x="107" y="242" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#EDEDED" text-anchor="middle">HAMBURGER ➔ CLOSE</text>
    <text x="107" y="260" font-family="'Inter', sans-serif" font-size="10" font-weight="500" fill="#8892B0" text-anchor="middle">Navigation State</text>
  </g>

  <!-- CARD 2: SUN ➔ MOON -->
  <g transform="translate(275, 80)">
    <rect width="215" height="280" rx="18" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
    <g transform="translate(107, 105)">
      <!-- Sun Rays -->
      <g stroke="#FFD000" stroke-width="3" stroke-linecap="round" transform="scale({ray_scale:.2f}) rotate({ray_rot:.1f})" opacity="{ray_scale:.2f}">
        <line x1="0" y1="-28" x2="0" y2="-23" />
        <line x1="0" y1="23" x2="0" y2="28" />
        <line x1="-28" y1="0" x2="-23" y2="0" />
        <line x1="23" y1="0" x2="28" y2="0" />
        <line x1="-20" y1="-20" x2="-16" y2="-16" />
        <line x1="16" y1="16" x2="20" y2="20" />
        <line x1="-20" y1="20" x2="-16" y2="16" />
        <line x1="16" y1="-16" x2="20" y2="-20" />
      </g>
      <!-- Center Circle with Mask -->
      <circle cx="0" cy="0" r="18" fill="{('#A0C4FF' if ease > 0.5 else '#FFD000')}" mask="url(#moon-mask-{f})" transform="rotate({moon_rot:.1f})" />
    </g>
    <text x="107" y="242" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#EDEDED" text-anchor="middle">SUN ➔ CRESCENT MOON</text>
    <text x="107" y="260" font-family="'Inter', sans-serif" font-size="10" font-weight="500" fill="#8892B0" text-anchor="middle">Theme Toggle</text>
  </g>

  <!-- CARD 3: PLAY ➔ PAUSE -->
  <g transform="translate(510, 80)">
    <rect width="215" height="280" rx="18" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
    <g transform="translate(107, 105)">
      <!-- Left bar / play left -->
      <rect x="{-bar_gap}" y="-16" width="{bar_w:.1f}" height="32" rx="3" fill="#FA5D29" />
      <!-- Right bar / play right -->
      <rect x="2" y="-16" width="{bar_w:.1f}" height="32" rx="3" fill="#EDEDED" />
    </g>
    <text x="107" y="242" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#EDEDED" text-anchor="middle">PLAY ➔ PAUSE ACTION</text>
    <text x="107" y="260" font-family="'Inter', sans-serif" font-size="10" font-weight="500" fill="#8892B0" text-anchor="middle">Media Playback</text>
  </g>

  <!-- CARD 4: DOWNLOAD ➔ CHECKMARK -->
  <g transform="translate(745, 80)">
    <rect width="215" height="280" rx="18" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
    <g transform="translate(107, 105)">
      <!-- Ring -->
      <circle cx="0" cy="0" r="22" fill="none" stroke="{('#34D399' if ease > 0.6 else '#49B3FC')}" stroke-width="3.5" stroke-dasharray="120" stroke-dashoffset="{int(80 * (1.0 - ease))}" transform="rotate({ring_rot:.1f})" />
      <!-- Arrow -->
      <g transform="translate(0, {arrow_y:.1f})" opacity="{arrow_opac:.2f}" stroke="#49B3FC">
        <line x1="0" y1="-10" x2="0" y2="8" stroke-width="3" stroke-linecap="round" />
        <path d="M -6 2 L 0 8 L 6 2" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
      </g>
      <!-- Checkmark -->
      <path d="M -8 1 L -2 7 L 8 -5" fill="none" stroke="#34D399" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="35" stroke-dashoffset="{check_dash:.1f}" opacity="{(1.0 if ease > 0.4 else 0.0)}" />
    </g>
    <text x="107" y="242" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#EDEDED" text-anchor="middle">DOWNLOAD ➔ CHECKMARK</text>
    <text x="107" y="260" font-family="'Inter', sans-serif" font-size="10" font-weight="500" fill="#8892B0" text-anchor="middle">Async Task Status</text>
  </g>
</svg>"""

        png_data = resvg_py.svg_to_bytes(frame_svg)
        frame_file = os.path.join(frame_dir, f"frame_{f:03d}.png")
        with open(frame_file, "wb") as f_out:
            f_out.write(png_data)

    out_mp4 = os.path.join(ROOT_DIR, "assets", "ui_icon_morphs.mp4")
    render_mp4(frame_dir, out_mp4, fps=fps)
    print(f"Generated 60 FPS Morphing Video MP4: {out_mp4}")
    return out_mp4

if __name__ == "__main__":
    generate_svg_and_png()
    render_morph_video_frames()
