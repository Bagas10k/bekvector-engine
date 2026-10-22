#!/usr/bin/env python3
"""
BekVector CLI — Command-line Interface for Procedural Vector Generation & Animation.
"""

import sys
import argparse
from bekvector import BekVector, render_png
from examples.bekbek_duck import create_duck
from examples.cyber_seal import create_seal
from examples.animated_sky import generate_sky_frame
from bekvector.animation import VectorAnimation

def main():
    parser = argparse.ArgumentParser(description="BekVector Engine — Procedural Vector & Animation Studio")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--duck", action="store_true", help="Generate Bekbek mascot duck vector")
    group.add_argument("--seal", action="store_true", help="Generate Cybernetic system seal vector")
    group.add_argument("--sky-anim", action="store_true", help="Generate 3-second procedural vector sky MP4 loop")

    parser.add_argument("--output", help="Output filepath (.svg, .png, or .mp4)")
    parser.add_argument("--png", help="Optional rasterized PNG output path")

    args = parser.parse_args()

    if args.duck:
        v = create_duck()
        svg = v.to_svg(bg="#0B0D13")
        out_svg = args.output or "bekbek_duck.svg"
        with open(out_svg, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated Bekbek Duck SVG: {out_svg}")
        if args.png:
            render_png(svg, args.png)
            print(f"Rasterized PNG: {args.png}")

    elif args.seal:
        v = create_seal()
        svg = v.to_svg(bg="#0A0B0E")
        out_svg = args.output or "cyber_seal.svg"
        with open(out_svg, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated Cyber Seal SVG: {out_svg}")
        if args.png:
            render_png(svg, args.png)
            print(f"Rasterized PNG: {args.png}")

    elif args.sky_anim:
        out_mp4 = args.output or "vektor_langit.mp4"
        anim = VectorAnimation(generate_sky_frame, total_frames=90, fps=30)
        anim.export_mp4(out_mp4)
        print(f"Generated Procedural Sky Animation: {out_mp4}")

if __name__ == "__main__":
    main()
