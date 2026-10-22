"""
BekVector Shaders & Procedural SVG Filters.
Zero-dependency SVG filter definitions: Analog Film Grain, Liquid Gooey, and Frosted Glass Glow.
"""

def get_grain_filter(filter_id: str = "filmGrain", base_frequency: float = 0.8, num_octaves: int = 3, opacity: float = 0.12) -> str:
    """Generates an analog film grain filter using SVG feTurbulence."""
    return f"""<filter id="{filter_id}">
  <feTurbulence type="fractalNoise" baseFrequency="{base_frequency}" numOctaves="{num_octaves}" stitchTiles="stitch" result="noise"/>
  <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 {opacity} 0" in="noise" result="grain"/>
  <feBlend mode="overlay" in="SourceGraphic" in2="grain"/>
</filter>"""

def get_gooey_filter(filter_id: str = "liquidGooey", blur_std: float = 8.0, matrix_contrast: float = 19.0) -> str:
    """Generates a liquid gooey morphing filter via feGaussianBlur and feColorMatrix."""
    return f"""<filter id="{filter_id}">
  <feGaussianBlur in="SourceGraphic" stdDeviation="{blur_std}" result="blur"/>
  <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 {matrix_contrast} -9" result="gooey"/>
  <feBlend in="SourceGraphic" in2="gooey"/>
</filter>"""

def get_frosted_specular_filter(filter_id: str = "specularGlow", surface_scale: float = 2.0) -> str:
    """Generates a subtle specular light reflection filter simulating polished glass."""
    return f"""<filter id="{filter_id}">
  <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur"/>
  <feSpecularLighting in="blur" surfaceScale="{surface_scale}" specularConstant="1.2" specularExponent="20" lighting-color="#FFFFFF" result="spec">
    <fePointLight x="-500" y="-1000" z="800"/>
  </feSpecularLighting>
  <feComposite in="spec" in2="SourceAlpha" operator="in" result="specOut"/>
  <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" k1="0" k2="1" k3="0.4" k4="0"/>
</filter>"""
