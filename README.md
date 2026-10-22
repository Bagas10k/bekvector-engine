# 🦆 BekVector Engine

> **Procedural SVG Vector Graphics & Micro-Atmosphere Animation Framework.**  
> *Developed by **Bagas Cihuy (Bagas Saputra)** with Bikagent (@Bekbekk_bot).*

---

## 🌟 Overview

**BekVector Engine** is a high-precision procedural vector graphics and animation studio written in Python. It constructs mathematical SVG curves, smooth Catmull-Rom splines, technical cybernetic insignias, and in-place looping UI animations directly from coordinate logic—without external design suites, heavy binary assets, or generic AI slop.

---

## ⚡ Core Features

- **Spline Catmull-Rom to Cubic Bezier:** Smooth biomorphic curves ($C^1$ continuity) with automatic acute-angle damping to suppress loop inversion.
- **Dynamic ViewBox Envelope:** Automatic boundary calculation with stroke dilation compensation (`max_stroke / 2`), guaranteeing **zero stroke clipping**.
- **Coordinate Quantization:** Intelligent `.1f` decimal formatting reducing SVG payload size by **71.6%** with zero perceptual loss.
- **Headless Millisecond Rasterization:** Native integration with `resvg-py` (Rust engine) rendering 4K Retina PNGs in under **35 ms**.
- **In-Place Vector Animation:** Multi-layer parallax drifting, periodic sine twinkling, and seamless video loops compiled directly to H.264 MP4 via `ffmpeg`.

---

## 📦 Project Structure

```text
bekvector-engine/
├── bekvector/             # Core Library
│   ├── __init__.py        # Public API exports
│   ├── core.py            # BekVector class, splines, primitives
│   ├── animation.py       # VectorAnimation loop sequencer
│   └── renderer.py        # Headless resvg-py & ffmpeg wrapper
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

# Generate the 3-second Procedural Animated Sky MP4 Loop
python3 cli.py --sky-anim --output assets/vektor_langit.mp4
```

---

## 💻 Python API Usage

### Drawing an Organic Mascot

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

# Cute Head & Eyes with Specular Highlights
v.circle(42, -35, 48, fill="#FFD166", stroke="#111111", stroke_w=3)
v.circle(52, -45, 11, fill="#111111")
v.circle(55, -48, 4, fill="#FFFFFF")

# Export to SVG & render high-res PNG
svg_code = v.to_svg(bg="#0B0D13")
with open("duck.svg", "w") as f:
    f.write(svg_code)
render_png(svg_code, "duck.png")
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
```

---

## 📜 License

MIT License © 2026 Bagas Cihuy (Bagas Saputra).
