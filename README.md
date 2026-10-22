# 🦆 BekVector Engine

> **Procedural SVG Vector Graphics, DataViz & Micro-Atmosphere Animation Framework.**  
> *Developed by **Bagas Cihuy (Bagas Saputra)** with Bikagent (@Bekbekk_bot).*

---

## 🌟 Overview

**BekVector Engine** is an enterprise-grade procedural vector graphics and animation studio written in Python. It constructs mathematical SVG curves, smooth Catmull-Rom splines, technical cybernetic insignias, telemetric data charts, and in-place looping UI animations directly from coordinate logic—without external design suites, heavy binary assets, or generic AI slop.

---

## ⚡ Core Superpowers

1. **Spline Catmull-Rom to Cubic Bezier:** Smooth biomorphic curves ($C^1$ continuity) with automatic acute-angle damping to suppress loop inversion.
2. **Dynamic ViewBox Envelope:** Automatic boundary calculation with stroke dilation compensation (`max_stroke / 2`), guaranteeing **zero stroke clipping**.
3. **Coordinate Quantization:** Intelligent `.1f` decimal formatting reducing SVG payload size by **71.6%** with zero perceptual loss.
4. **Standalone SVG Animator (0 KB Video):** Pure CSS `@keyframes` embedded inside SVG, enabling continuous 60 FPS animation without HTML5 video players or JavaScript.
5. **DataViz & Telemetry Engine:** Zero-dependency SVG sparkline trendlines, polar spider/radar charts, and activity tickers.
6. **Procedural Shaders & Filters:** In-code SVG filters for analog film grain (`feTurbulence`), liquid gooey morphing (`feColorMatrix`), and frosted glass specular reflections.
7. **Spring Physics Engine:** Second-order harmonic oscillator ($F = -kx - cv$) for natural jelly bounce and tactile overshoot.
8. **Frontend Exporter:** One-command compilation of SVG markup directly into React (`.jsx` / `.tsx`) and Vue 3 SFC components.
9. **Interactive Web Studio:** Built-in dark-mode web workbench (`cli.py --studio`) for live asset preview, parameter tweaking, and instant exports.

---

## 📦 Project Structure

```text
bekvector-engine/
├── bekvector/             # Core Library
│   ├── __init__.py        # Public API exports
│   ├── core.py            # BekVector canvas, splines, primitives
│   ├── animation.py       # Multi-frame video loop sequencer
│   ├── renderer.py        # Headless resvg-py & ffmpeg wrapper
│   ├── dataviz.py         # Sparklines, radar charts, data bars
│   ├── svg_animator.py    # Pure CSS standalone SVG animations
│   ├── filters.py         # SVG shaders: Film grain, liquid gooey
│   ├── themes.py          # Parametric palette presets (WCAG AAA)
│   ├── spring.py          # Second-order elastic physics engine
│   ├── exporter.py        # React & Vue component exporter
│   └── studio.py          # Embedded interactive web studio
├── examples/              # Showcase Generators
│   ├── bekbek_duck.py     # Iconic Bekbek mascot duck
│   ├── cyber_seal.py      # Cybernetic system insignia seal
│   └── animated_sky.py    # 3-second procedural vector sky MP4 loop
├── assets/                # Rendered Master Outputs (SVG, PNG, MP4)
├── tests/                 # Unit Tests (100% Passing)
├── cli.py                 # Interactive CLI tool
└── requirements.txt       # Dependencies (resvg-py)
```

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/Bagas10k/bekvector-engine.git
cd bekvector-engine
pip install -r requirements.txt
```

### 2. Generate Vector Assets via CLI

```bash
# Generate the iconic Bekbek Mascot Duck (SVG + PNG)
python3 cli.py --duck --output assets/bekbek_duck.svg --png assets/bekbek_duck.png

# Generate a Cybernetic System Seal
python3 cli.py --seal --output assets/cyber_seal.svg --png assets/cyber_seal.png

# Generate a Pure CSS Animated Weather SVG (0 KB video)
python3 cli.py --weather-svg --output assets/animated_weather.svg

# Generate Telemetry Sparkline & Radar Charts
python3 cli.py --sparkline --output assets/sparkline.svg --png assets/sparkline.png
python3 cli.py --radar --output assets/radar.svg --png assets/radar.png

# Generate the 3-second Procedural Animated Sky MP4 Loop
python3 cli.py --sky-anim --output assets/vektor_langit.mp4
```

### 3. Launch Interactive Web Studio

```bash
python3 cli.py --studio --port 3095
# Open http://localhost:3095 in your browser
```

---

## 💻 Python API Usage

### 1. Drawing an Organic Mascot

```python
from bekvector import BekVector, render_png

v = BekVector(min_padding=20)
# Body spline with Catmull-Rom smoothing
body_pts = [
    (-90, 40), (-115, 20), (-80, 50), (-40, 85),
    (20, 88), (75, 70), (90, 40), (85, 10),
    (40, -10), (-10, 10), (-60, 25)
]
v.path(body_pts, fill="#FFD166", stroke="#111111", stroke_w=3, smooth=0.35)
v.circle(42, -35, 48, fill="#FFD166", stroke="#111111", stroke_w=3)
v.circle(52, -45, 11, fill="#111111")
v.circle(55, -48, 4, fill="#FFFFFF")

svg_code = v.to_svg(bg="#0B0D13")
render_png(svg_code, "duck.png")
```

### 2. Telemetry Sparkline & React Export

```python
from bekvector import DataViz, to_react_component

# Generate 496-byte sparkline SVG
svg_chart = DataViz.sparkline([12, 19, 15, 28, 35, 42, 38, 55, 68, 74], stroke="#10B981")

# Export directly to React TypeScript Component
tsx_code = to_react_component(svg_chart, component_name="TelemetrySparkline", typescript=True)
with open("TelemetrySparkline.tsx", "w") as f:
    f.write(tsx_code)
```

---

## 📐 Mathematical Foundations

### Acute Angle Spline Damping
When converting polygon sequences to cubic Bezier segments, sharp turns ($\theta < 45^\circ$) can produce tangent overshoot loops. BekVector dampens tangent magnitude proportionally to the angle cosine:
$$\text{damping} = 1.0 - \left(\frac{\theta}{\pi}\right) \cdot 0.65$$
$$\text{effective\_smooth} = \text{base\_smooth} \cdot \max(0.2, \text{damping})$$

### ViewBox Envelope
$$\text{dilation} = \max\left( \frac{\text{stroke\_width}}{2}, 6\text{px} \right)$$
$$\text{pad} = \max(\text{min\_padding}, \lceil \text{dilation} \rceil)$$

---

## 🧪 Testing

Run automated unit tests:

```bash
python3 -m unittest discover tests
# Ran 9 tests in 0.002s -> OK
```

---

## 📜 License

MIT License © 2026 Bagas Cihuy (Bagas Saputra).
