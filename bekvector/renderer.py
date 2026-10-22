"""
BekVector Renderer — High-Speed Headless PNG & MP4 Output.
"""

import os
import subprocess
from typing import Optional

def render_png(svg_string: str, output_path: str) -> str:
    """Renders SVG to crisp PNG in milliseconds using resvg-py."""
    import resvg_py
    png_bytes = resvg_py.svg_to_bytes(svg_string)
    with open(output_path, "wb") as f:
        f.write(png_bytes)
    return output_path

def render_mp4(frame_dir: str, output_path: str, fps: int = 30) -> str:
    """Compiles a sequential series of PNG frames into a compressed H.264 MP4."""
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frame_dir, "frame_%03d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path
