"""
bekvector/character.py - Parametric Ligne Claire Character & Mascot Generator.
Procedurally generates editorial vector character portraits with companion mascots,
customizable outfits, postures, and brand identity cards.
"""

class CharacterCardBuilder:
    def __init__(self, name="Bagas Saputra", role="Founder & Creative Director", email="bagas.office01@gmail.com"):
        self.name = name
        self.role = role
        self.email = email
        self.card_color = "#FFD000"
        self.bg_color = "#E65100"
        self.mascot_type = "sasi_kedi" # or "bekbek_duck"
        self.has_glasses = True
        self.outfit = "streetwear"

    def set_mascot(self, mascot_type="sasi_kedi"):
        self.mascot_type = mascot_type
        return self

    def set_colors(self, card_color="#FFD000", bg_color="#E65100"):
        self.card_color = card_color
        self.bg_color = bg_color
        return self

    def generate_svg(self, width=700, height=1120):
        # Build parametric SVG
        mascot_svg = self._render_sasi_kedi() if self.mascot_type == "sasi_kedi" else self._render_bekbek()
        glasses_svg = self._render_glasses() if self.has_glasses else ""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <filter id="cardShadow" x="-15%" y="-10%" width="130%" height="130%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="16" result="blur1" />
      <feOffset in="blur1" dx="0" dy="18" result="offset1" />
      <feFlood flood-color="#802000" flood-opacity="0.32" result="color1" />
      <feComposite in="color1" in2="offset1" operator="in" result="shadow1" />
      <feMerge>
        <feMergeNode in="shadow1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <rect width="{width}" height="{height}" fill="{self.bg_color}" />

  <g transform="translate(65, 55)" filter="url(#cardShadow)">
    <rect width="570" height="1010" rx="32" fill="{self.card_color}" />

    <!-- Typography -->
    <text x="52" y="92" font-family="'Inter', Arial, sans-serif" font-size="34" font-weight="900" fill="#141414" letter-spacing="-0.02em">
      {self.name}
    </text>
    <text x="52" y="132" font-family="'Inter', Arial, sans-serif" font-size="20" font-weight="500" fill="#584500">
      {self.role}
    </text>

    <!-- Vertical Email -->
    <g transform="translate(528, 540) rotate(-90)">
      <text x="0" y="0" font-family="'JetBrains Mono', monospace" font-size="15" font-weight="600" fill="#483800" letter-spacing="0.08em">
        {self.email}
      </text>
    </g>

    <!-- Character Body -->
    <g transform="translate(30, 180)">
      <!-- Trousers -->
      <path d="M 120 720 L 135 630 C 145 615 155 610 200 610 L 320 610 C 360 610 375 615 385 630 L 400 720 Z" fill="#161616" />
      <!-- Left Arm in Pocket -->
      <path d="M 95 410 C 85 460 90 530 115 600 C 125 625 140 640 160 645 L 160 620 C 140 610 130 540 135 440 Z" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" stroke-linejoin="round" />
      
      <!-- Torso Boxy Tee -->
      <path d="M 130 405 C 170 380 230 375 270 375 C 330 375 385 390 415 420 L 390 620 C 330 635 190 635 135 620 Z" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" stroke-linejoin="round" />
      
      <!-- Utility Strap -->
      <path d="M 175 380 L 375 625 L 340 630 L 145 390 Z" fill="#141414" />
      <rect x="235" y="475" width="45" height="28" rx="6" fill="#FFD000" stroke="#141414" stroke-width="3" transform="rotate(38 235 475)" />

      <!-- Compression Creases under Cat -->
      <path d="M 190 470 C 220 480 240 482 255 480" fill="none" stroke="#141414" stroke-width="2.8" stroke-linecap="round" />
      <path d="M 180 500 C 210 515 240 520 265 515" fill="none" stroke="#141414" stroke-width="2.8" stroke-linecap="round" />

      <!-- Neck -->
      <path d="M 228 375 L 228 295 L 292 295 L 292 375 Z" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" />
      <!-- Cradling Arm -->
      <path d="M 410 425 C 430 475 425 540 375 565 C 320 585 245 572 195 542 C 185 532 190 515 208 515 C 245 535 305 545 345 530 C 375 515 380 475 375 435 Z" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" stroke-linejoin="round" />
      <path d="M 198 520 C 188 525 184 540 194 545 C 208 552 222 545 232 535" fill="#FFFFFF" stroke="#141414" stroke-width="3.5" />

      <!-- Face -->
      <path d="M 200 185 L 200 235 C 200 288 230 318 268 318 C 306 318 335 288 335 235 L 335 185 Z" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" stroke-linejoin="round" />
      {glasses_svg}
      <circle cx="238" cy="222" r="4.5" fill="#141414" />
      <circle cx="284" cy="222" r="4.5" fill="#141414" />
      <path d="M 262 215 L 264 246 L 254 252 L 266 252" fill="none" stroke="#141414" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M 245 275 C 258 288 268 288 280 275" fill="none" stroke="#141414" stroke-width="3.8" stroke-linecap="round" />

      <!-- Hair -->
      <path d="M 195 200 C 188 135 220 95 272 90 C 335 85 358 128 350 200 C 344 165 328 140 285 136 C 238 132 212 160 205 195 Z" fill="#141414" stroke="#141414" stroke-width="3" />
      <path d="M 250 92 C 262 82 284 84 294 94" fill="none" stroke="#141414" stroke-width="3.5" stroke-linecap="round" />

      <!-- Companion Mascot -->
      {mascot_svg}
    </g>
  </g>
</svg>"""
        return svg

    def _render_glasses(self):
        return """
      <circle cx="236" cy="222" r="19" fill="#FFFFFF" stroke="#141414" stroke-width="3.5" />
      <circle cx="286" cy="222" r="19" fill="#FFFFFF" stroke="#141414" stroke-width="3.5" />
      <line x1="255" y1="220" x2="267" y2="220" stroke="#141414" stroke-width="3.5" stroke-linecap="round" />
      <line x1="217" y1="220" x2="198" y2="216" stroke="#141414" stroke-width="3" stroke-linecap="round" />
      <line x1="305" y1="220" x2="330" y2="216" stroke="#141414" stroke-width="3" stroke-linecap="round" />
"""

    def _render_sasi_kedi(self):
        return """
      <g id="living-sasi-kedi" transform="translate(250, 310)">
        <path d="M 140 180 C 190 220 180 320 120 330 C 80 335 75 300 105 295 C 135 290 140 240 105 210 Z" fill="#141414" />
        <path d="M 15 80 C 5 150 45 200 115 200 C 175 200 195 145 190 90 C 185 45 150 20 105 20 C 55 20 15 35 15 80 Z" fill="#141414" stroke="#141414" stroke-width="4.5" />
        <path d="M 32 155 C 20 172 26 195 45 195 C 60 195 66 178 60 160 Z" fill="#141414" stroke="#FFD000" stroke-width="2.5" />
        <path d="M 72 170 C 65 188 74 205 90 205 C 105 205 108 188 102 170 Z" fill="#141414" stroke="#FFD000" stroke-width="2.5" />
        <path d="M 30 35 C 18 -5 40 -45 48 -55 C 56 -65 68 -45 76 -25 C 102 -35 135 -35 155 -22 C 166 -40 178 -62 188 -52 C 196 -42 205 -5 195 30 C 205 75 175 120 110 120 C 50 120 18 75 30 35 Z" fill="#141414" stroke="#141414" stroke-width="4.5" />
        <circle cx="82" cy="40" r="28" fill="#FFFFFF" stroke="#141414" stroke-width="3" />
        <circle cx="142" cy="40" r="28" fill="#FFFFFF" stroke="#141414" stroke-width="3" />
        <circle cx="100" cy="43" r="10.5" fill="#141414" />
        <circle cx="103" cy="39" r="3.2" fill="#FFFFFF" />
        <circle cx="124" cy="41" r="10.5" fill="#141414" />
        <circle cx="127" cy="37" r="3.2" fill="#FFFFFF" />
        <polygon points="112,60 106,53 118,53" fill="#FFFFFF" />
        <path d="M 54 54 C 34 50 14 52 -2 60" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
        <path d="M 52 64 C 30 65 10 70 -6 78" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
        <path d="M 170 54 C 190 50 210 52 226 60" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
        <path d="M 172 64 C 194 65 214 70 230 78" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
      </g>
"""

    def _render_bekbek(self):
        # Companion Bekbek Duck
        return """
      <g id="companion-bekbek" transform="translate(250, 310)">
        <ellipse cx="100" cy="120" rx="70" ry="55" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" />
        <circle cx="70" cy="50" r="38" fill="#FFFFFF" stroke="#141414" stroke-width="4.5" />
        <path d="M 35 48 C 15 50 0 65 20 72 C 40 76 50 68 55 58 Z" fill="#FA5D29" stroke="#141414" stroke-width="3" />
        <circle cx="68" cy="42" r="5" fill="#141414" />
        <circle cx="70" cy="40" r="1.5" fill="#FFFFFF" />
      </g>
"""
