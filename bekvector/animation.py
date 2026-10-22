"""
BekVector Animation — Procedural In-Place Looping Engine.
Generates multi-frame seamless vector animation loops for web UI and video.
"""

import os
import shutil
from typing import Callable
from .core import BekVector
from .renderer import render_png, render_mp4

class VectorAnimation:
    def __init__(self, generator_fn: Callable[[float], BekVector], total_frames: int = 90, fps: int = 30):
        self.generator_fn = generator_fn
        self.total_frames = total_frames
        self.fps = fps

    def export_mp4(self, output_path: str, temp_dir: str = "/tmp/bekvector_frames") -> str:
        """Renders frames and compiles MP4 video loop."""
        os.makedirs(temp_dir, exist_ok=True)
        try:
            for idx in range(self.total_frames):
                t_norm = idx / self.total_frames
                vec = self.generator_fn(t_norm)
                svg_data = vec.to_svg() if hasattr(vec, "to_svg") else str(vec)
                frame_path = os.path.join(temp_dir, f"frame_{idx:03d}.png")
                render_png(svg_data, frame_path)
            render_mp4(temp_dir, output_path, fps=self.fps)
            return output_path
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
