"""
BekVector Themes — Parametric Palettes & WCAG Contrast Assurance.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class Theme:
    name: str
    bg: str
    surface: str
    border: str
    text_primary: str
    text_muted: str
    accent_primary: str
    accent_secondary: str

THEMES: Dict[str, Theme] = {
    "cyber_ember": Theme(
        name="Cyber Ember",
        bg="#0A0B0E",
        surface="#12151D",
        border="rgba(255, 255, 255, 0.08)",
        text_primary="#EDEDED",
        text_muted="#8E9AA8",
        accent_primary="#FA5D29",
        accent_secondary="#49B3FC"
    ),
    "swiss_editorial": Theme(
        name="Swiss Editorial",
        bg="#F8F9FA",
        surface="#FFFFFF",
        border="#111111",
        text_primary="#111111",
        text_muted="#666666",
        accent_primary="#FA5D29",
        accent_secondary="#0047AB"
    ),
    "neon_matrix": Theme(
        name="Neon Matrix",
        bg="#050807",
        surface="#0D1410",
        border="rgba(166, 255, 0, 0.15)",
        text_primary="#F0FFF4",
        text_muted="#7BA385",
        accent_primary="#A6FF00",
        accent_secondary="#00F0FF"
    ),
    "warm_obsidian": Theme(
        name="Warm Obsidian",
        bg="#0D0E12",
        surface="#16181F",
        border="rgba(255, 255, 255, 0.07)",
        text_primary="#F4F4F6",
        text_muted="#9A9EAC",
        accent_primary="#FFD166",
        accent_secondary="#FA5D29"
    ),
    "pastel_kawaii": Theme(
        name="Pastel Kawaii",
        bg="#10121A",
        surface="#1B1E2B",
        border="rgba(255, 209, 102, 0.15)",
        text_primary="#FFFFFF",
        text_muted="#A0A5BC",
        accent_primary="#FFD166",
        accent_secondary="#FF85A1"
    )
}

def get_theme(name: str = "cyber_ember") -> Theme:
    return THEMES.get(name.lower(), THEMES["cyber_ember"])
