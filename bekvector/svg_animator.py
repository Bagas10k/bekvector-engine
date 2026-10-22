"""
BekVector Standalone SVG Animator — Pure CSS Keyframe Animation Generator.
Produces self-contained animated SVGs that loop natively at 60 FPS without video players or JavaScript.
"""

def generate_animated_weather_svg(condition: str = "night_sky", width: int = 400, height: int = 240) -> str:
    """Generates a standalone animated SVG with inline CSS @keyframes."""
    if condition == "night_sky":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#080A10"/>
      <stop offset="100%" stop-color="#1B1E2D"/>
    </linearGradient>
    <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgba(255,235,180,0.3)"/>
      <stop offset="100%" stop-color="rgba(255,235,180,0)"/>
    </radialGradient>
  </defs>

  <style>
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    @keyframes driftBack {{
      0% {{ transform: translateX(-80px); }}
      100% {{ transform: translateX({width + 80}px); }}
    }}
    @keyframes driftFront {{
      0% {{ transform: translateX(-120px); }}
      100% {{ transform: translateX({width + 120}px); }}
    }}
    @keyframes moonFloat {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-5px); }}
    }}
    @keyframes meteor {{
      0% {{ transform: translate(0, 0); opacity: 0; }}
      15% {{ opacity: 1; }}
      35% {{ transform: translate(-140px, 80px); opacity: 0; }}
      100% {{ transform: translate(-140px, 80px); opacity: 0; }}
    }}
    .star-1 {{ animation: twinkle 2.2s infinite ease-in-out; transform-origin: 60px 40px; }}
    .star-2 {{ animation: twinkle 3.1s infinite ease-in-out 0.8s; transform-origin: 180px 70px; }}
    .star-3 {{ animation: twinkle 2.6s infinite ease-in-out 1.4s; transform-origin: 290px 45px; }}
    .cloud-slow {{ animation: driftBack 32s linear infinite; }}
    .cloud-fast {{ animation: driftFront 18s linear infinite; }}
    .moon-group {{ animation: moonFloat 5s ease-in-out infinite; }}
    .shooting-star {{ animation: meteor 6s linear infinite 2s; }}
  </style>

  <!-- Sky Canvas -->
  <rect width="{width}" height="{height}" rx="16" fill="url(#bg)"/>

  <!-- Twinkling Stars -->
  <circle cx="60" cy="40" r="2" fill="#FFF" class="star-1"/>
  <circle cx="180" cy="70" r="1.5" fill="#FFF" class="star-2"/>
  <circle cx="290" cy="45" r="2" fill="#FFF" class="star-3"/>
  <circle cx="120" cy="95" r="1.5" fill="#FFF" class="star-1"/>
  <circle cx="340" cy="85" r="1.8" fill="#FFF" class="star-2"/>

  <!-- Shooting Star -->
  <line x1="280" y1="20" x2="310" y2="5" stroke="#FA5D29" stroke-width="2" stroke-linecap="round" class="shooting-star"/>

  <!-- Floating Moon -->
  <g class="moon-group">
    <circle cx="310" cy="65" r="32" fill="url(#moonGlow)"/>
    <circle cx="310" cy="65" r="18" fill="#FFE8A3"/>
    <circle cx="304" cy="60" r="16" fill="#121520"/>
  </g>

  <!-- Cloud Layers -->
  <g class="cloud-slow">
    <path d="M 0 160 Q 30 135 60 142 Q 90 120 120 142 Q 150 135 180 160 Z" fill="rgba(45, 52, 75, 0.45)"/>
  </g>
  <g class="cloud-fast">
    <path d="M 0 190 Q 40 160 80 170 Q 120 145 160 170 Q 200 160 240 190 Z" fill="rgba(20, 24, 38, 0.85)"/>
  </g>

  <!-- Hairline Border -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="15" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
</svg>"""

    return ""
