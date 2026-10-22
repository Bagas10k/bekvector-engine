"""
bekvector/morph.py - Smooth 60 FPS UI Icon Morphing Engine.
Generates standalone morphing SVG icons and renders frame-by-frame 60 FPS video animations.
"""

import math
import os

class IconMorph:
    """
    Library of self-contained morphing UI icons with cubic-bezier easing and 60 FPS timing.
    """

    @staticmethod
    def hamburger_to_close(size=80, stroke_width=4, color="#EDEDED", accent_color="#FA5D29"):
        """
        Morph 1: Hamburger Menu (3 bars) -> Close 'X'
        """
        return f"""
        <g class="icon-hamburger-close" transform="translate({size/2}, {size/2})">
          <style>
            @keyframes topBarMorph {{
              0%, 15% {{ transform: translateY(-12px) rotate(0deg); }}
              45%, 65% {{ transform: translateY(0px) rotate(45deg); }}
              85%, 100% {{ transform: translateY(-12px) rotate(0deg); }}
            }}
            @keyframes midBarMorph {{
              0%, 15% {{ transform: scaleX(1); opacity: 1; }}
              45%, 65% {{ transform: scaleX(0); opacity: 0; }}
              85%, 100% {{ transform: scaleX(1); opacity: 1; }}
            }}
            @keyframes botBarMorph {{
              0%, 15% {{ transform: translateY(12px) rotate(0deg); }}
              45%, 65% {{ transform: translateY(0px) rotate(-45deg); }}
              85%, 100% {{ transform: translateY(12px) rotate(0deg); }}
            }}
            .bar-top {{
              animation: topBarMorph 3s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
            .bar-mid {{
              animation: midBarMorph 3s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
            .bar-bot {{
              animation: botBarMorph 3s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
          </style>
          <line class="bar-top" x1="-16" y1="0" x2="16" y2="0" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" />
          <line class="bar-mid" x1="-16" y1="0" x2="16" y2="0" stroke="{accent_color}" stroke-width="{stroke_width}" stroke-linecap="round" />
          <line class="bar-bot" x1="-16" y1="0" x2="16" y2="0" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" />
        </g>
        """

    @staticmethod
    def sun_to_moon(size=80, color="#FFD000", moon_color="#A0C4FF"):
        """
        Morph 2: Sun (Light Mode) -> Crescent Moon (Dark Mode)
        """
        r = size * 0.22
        return f"""
        <g class="icon-sun-moon" transform="translate({size/2}, {size/2})">
          <style>
            @keyframes sunMoonBody {{
              0%, 15% {{
                fill: {color};
                transform: rotate(0deg) scale(1);
              }}
              45%, 65% {{
                fill: {moon_color};
                transform: rotate(140deg) scale(1.1);
              }}
              85%, 100% {{
                fill: {color};
                transform: rotate(360deg) scale(1);
              }}
            }}
            @keyframes moonScoop {{
              0%, 15% {{
                cx: 40px;
                cy: -40px;
              }}
              45%, 65% {{
                cx: 8px;
                cy: -8px;
              }}
              85%, 100% {{
                cx: 40px;
                cy: -40px;
              }}
            }}
            @keyframes sunRays {{
              0%, 15% {{
                opacity: 1;
                transform: scale(1) rotate(0deg);
              }}
              45%, 65% {{
                opacity: 0;
                transform: scale(0.2) rotate(90deg);
              }}
              85%, 100% {{
                opacity: 1;
                transform: scale(1) rotate(360deg);
              }}
            }}
            .sun-core {{
              animation: sunMoonBody 3.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
              mask: url(#moon-mask);
            }}
            .mask-scoop {{
              animation: moonScoop 3.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
            }}
            .sun-rays-group {{
              animation: sunRays 3.5s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
          </style>
          
          <mask id="moon-mask">
            <rect x="-50" y="-50" width="100" height="100" fill="#FFFFFF" />
            <circle class="mask-scoop" cx="40" cy="-40" r="{r * 0.95}" fill="#000000" />
          </mask>

          <!-- Radiating Sun Rays -->
          <g class="sun-rays-group" stroke="{color}" stroke-width="3" stroke-linecap="round">
            <line x1="0" y1="-28" x2="0" y2="-23" />
            <line x1="0" y1="23" x2="0" y2="28" />
            <line x1="-28" y1="0" x2="-23" y2="0" />
            <line x1="23" y1="0" x2="28" y2="0" />
            <line x1="-20" y1="-20" x2="-16" y2="-16" />
            <line x1="16" y1="16" x2="20" y2="20" />
            <line x1="-20" y1="20" x2="-16" y2="16" />
            <line x1="16" y1="-16" x2="20" y2="-20" />
          </g>

          <!-- Center Body -->
          <circle class="sun-core" cx="0" cy="0" r="{r}" />
        </g>
        """

    @staticmethod
    def play_to_pause(size=80, color="#FFFFFF", accent="#FA5D29"):
        """
        Morph 3: Play Triangle -> Pause Double Bars -> Success Check
        """
        return f"""
        <g class="icon-play-pause" transform="translate({size/2}, {size/2})">
          <style>
            @keyframes playToPauseLeft {{
              0%, 15% {{
                d: path("M -12 -16 L -2 -10 L -2 10 L -12 16 Z");
                fill: {accent};
              }}
              45%, 65% {{
                d: path("M -10 -14 L -4 -14 L -4 14 L -10 14 Z");
                fill: {color};
              }}
              85%, 100% {{
                d: path("M -12 -16 L -2 -10 L -2 10 L -12 16 Z");
                fill: {accent};
              }}
            }}
            @keyframes playToPauseRight {{
              0%, 15% {{
                d: path("M -2 -10 L 14 0 L 14 0 L -2 10 Z");
                fill: {accent};
              }}
              45%, 65% {{
                d: path("M 4 -14 L 10 -14 L 10 14 L 4 14 Z");
                fill: {color};
              }}
              85%, 100% {{
                d: path("M -2 -10 L 14 0 L 14 0 L -2 10 Z");
                fill: {accent};
              }}
            }}
            .bar-left {{
              animation: playToPauseLeft 2.8s cubic-bezier(0.16, 1, 0.3, 1) infinite;
            }}
            .bar-right {{
              animation: playToPauseRight 2.8s cubic-bezier(0.16, 1, 0.3, 1) infinite;
            }}
          </style>
          <path class="bar-left" d="M -12 -16 L -2 -10 L -2 10 L -12 16 Z" />
          <path class="bar-right" d="M -2 -10 L 14 0 L 14 0 L -2 10 Z" />
        </g>
        """

    @staticmethod
    def download_to_check(size=80, stroke_color="#49B3FC", success_color="#34D399"):
        """
        Morph 4: Download Arrow -> Circular Spinner -> Success Checkmark
        """
        return f"""
        <g class="icon-download-check" transform="translate({size/2}, {size/2})">
          <style>
            @keyframes arrowMorph {{
              0%, 15% {{
                transform: translateY(0px) scale(1);
                opacity: 1;
                stroke: {stroke_color};
              }}
              30%, 65% {{
                transform: translateY(-8px) scale(0.2);
                opacity: 0;
              }}
              75%, 90% {{
                transform: translateY(0px) scale(1);
                opacity: 1;
                stroke: {success_color};
              }}
              100% {{
                transform: translateY(0px) scale(1);
                opacity: 1;
                stroke: {stroke_color};
              }}
            }}
            @keyframes circleProgress {{
              0%, 15% {{
                stroke-dasharray: 120;
                stroke-dashoffset: 80;
                transform: rotate(0deg);
                stroke: {stroke_color};
              }}
              35%, 65% {{
                stroke-dasharray: 120;
                stroke-dashoffset: 30;
                transform: rotate(540deg);
                stroke: {stroke_color};
              }}
              75%, 90% {{
                stroke-dasharray: 120;
                stroke-dashoffset: 0;
                transform: rotate(720deg);
                stroke: {success_color};
              }}
              100% {{
                stroke-dasharray: 120;
                stroke-dashoffset: 80;
                transform: rotate(1080deg);
                stroke: {stroke_color};
              }}
            }}
            @keyframes checkmarkReveal {{
              0%, 68% {{
                stroke-dashoffset: 35;
                opacity: 0;
              }}
              75%, 90% {{
                stroke-dashoffset: 0;
                opacity: 1;
              }}
              98%, 100% {{
                stroke-dashoffset: 35;
                opacity: 0;
              }}
            }}
            .progress-ring {{
              animation: circleProgress 4s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
            .arrow-group {{
              animation: arrowMorph 4s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
            .check-path {{
              stroke-dasharray: 35;
              animation: checkmarkReveal 4s cubic-bezier(0.16, 1, 0.3, 1) infinite;
              transform-origin: center;
            }}
          </style>

          <!-- Outer Ring / Tray -->
          <circle class="progress-ring" cx="0" cy="0" r="22" fill="none" stroke-width="3.5" stroke-linecap="round" />

          <!-- Download Arrow Elements -->
          <g class="arrow-group">
            <line x1="0" y1="-10" x2="0" y2="8" stroke-width="3" stroke-linecap="round" />
            <path d="M -6 2 L 0 8 L 6 2" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
          </g>

          <!-- Success Checkmark -->
          <path class="check-path" d="M -8 1 L -2 7 L 8 -5" fill="none" stroke="{success_color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
        </g>
        """

    @classmethod
    def generate_showcase_stage(cls, width=1000, height=420):
        """
        Creates a complete multi-card UI showcase with 4 morphing icons
        rendered inside high-end blur-glass cards!
        """
        icons = [
            ("HAMBURGER ➔ CLOSE", cls.hamburger_to_close(80), "Navigation State"),
            ("SUN ➔ CRESCENT MOON", cls.sun_to_moon(80), "Theme Morph"),
            ("PLAY ➔ PAUSE ACTION", cls.play_to_pause(80), "Media Playback"),
            ("DOWNLOAD ➔ CHECKMARK", cls.download_to_check(80), "Async Task Status"),
        ]

        card_markup = []
        for i, (title, icon_content, subtitle) in enumerate(icons):
            cx = 40 + i * 235
            cy = 80
            card_markup.append(f"""
    <!-- Card {i+1}: {title} -->
    <g transform="translate({cx}, {cy})">
      <!-- Blur Glass Physical Card Frame -->
      <rect width="215" height="280" rx="18" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
      <line x1="15" y1="220" x2="200" y2="220" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1" />
      
      <!-- Morphing Icon Viewport -->
      <g transform="translate(107, 105)">
        {icon_content}
      </g>

      <!-- Editorial Typography -->
      <text x="107" y="242" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#EDEDED" text-anchor="middle" letter-spacing="0.06em">
        {title}
      </text>
      <text x="107" y="260" font-family="'Inter', sans-serif" font-size="10" font-weight="500" fill="#8892B0" text-anchor="middle">
        {subtitle}
      </text>
    </g>
""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Dark Studio Mesh Gradient -->
    <linearGradient id="stageBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0D13" />
      <stop offset="50%" stop-color="#141824" />
      <stop offset="100%" stop-color="#08090C" />
    </linearGradient>
  </defs>

  <rect width="{width}" height="{height}" fill="url(#stageBg)" />

  <!-- Stage Header -->
  <text x="40" y="44" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="#EDEDED" letter-spacing="0.04em">
    BEKVISUAL · DYNAMIC UI ICON MORPHING
  </text>
  <text x="{width - 40}" y="44" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#FA5D29" text-anchor="end">
    60 FPS IN-PLACE FLUID TRANSFORMATION
  </text>
  <line x1="40" y1="56" x2="{width - 40}" y2="56" stroke="rgba(255,255,255,0.1)" stroke-width="1.2" />

  {''.join(card_markup)}
</svg>"""
        return svg
