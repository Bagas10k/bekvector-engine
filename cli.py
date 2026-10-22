#!/usr/bin/env python3
"""
BekVector CLI — Command-line Interface for Procedural Vector Generation & Animation.
"""

import sys
import argparse
from bekvector import (
    BekVector, render_png, DataViz, generate_animated_weather_svg,
    to_react_component, run_studio
)
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
    group.add_argument("--weather-svg", action="store_true", help="Generate pure CSS animated weather SVG (0 KB video)")
    group.add_argument("--sparkline", action="store_true", help="Generate telemetry data sparkline SVG")
    group.add_argument("--radar", action="store_true", help="Generate polar radar/spider chart SVG")
    group.add_argument("--text-anim", help="Convert text string into animated vector shape SVG (e.g. --text-anim 'BEKVEKTOR')")
    group.add_argument("--morph", action="store_true", help="Generate 60 FPS UI icon morphing showcase (SVG/PNG/MP4)")
    group.add_argument("--studio", action="store_true", help="Launch live interactive web workbench")

    parser.add_argument("--output", help="Output filepath (.svg, .png, .mp4, or .jsx)")
    parser.add_argument("--png", help="Optional rasterized PNG output path")
    parser.add_argument("--react", help="Optional React JSX component output path")
    parser.add_argument("--port", type=int, default=3095, help="Port for Studio web server (default: 3095)")

    args = parser.parse_args()

    if args.studio:
        run_studio(port=args.port)
        return

    svg = ""
    out_name = "asset.svg"

    if args.duck:
        v = create_duck()
        svg = v.to_svg(bg="#0B0D13")
        out_name = "bekbek_duck.svg"
    elif args.seal:
        v = create_seal()
        svg = v.to_svg(bg="#0A0B0E")
        out_name = "cyber_seal.svg"
    elif args.weather_svg:
        svg = generate_animated_weather_svg("night_sky", 480, 280)
        out_name = "animated_weather.svg"
    elif args.sparkline:
        svg = DataViz.sparkline([15, 22, 18, 32, 45, 38, 52, 68, 75], width=360, height=100)
        out_name = "sparkline_telemetry.svg"
    elif args.radar:
        svg = DataViz.radar_chart({"CPU": 45, "RAM": 44, "DISK": 70, "NET": 85, "ACC": 98}, radius=80)
        out_name = "radar_metrics.svg"
    elif args.text_anim:
        from bekvector.text import TextToPath
        svg = TextToPath.create_animated_text_svg(args.text_anim, font_size=72, accent_color="#FA5D29", accent_indices=[0, 1, 2], animation_type="stagger_rise")
        out_name = "text_vector.svg"
    elif args.morph:
        from bekvector.morph import IconMorph
        svg = IconMorph.generate_showcase_stage(1000, 420)
        out_name = "ui_icon_morphs.svg"
    elif args.sky_anim:
        out_mp4 = args.output or "vektor_langit.mp4"
        anim = VectorAnimation(generate_sky_frame, total_frames=90, fps=30)
        anim.export_mp4(out_mp4)
        print(f"Generated Procedural Sky Animation: {out_mp4}")
        return

    out_file = args.output or out_name
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated SVG: {out_file} ({len(svg)} bytes)")

    if args.png:
        render_png(svg, args.png)
        print(f"Rasterized PNG: {args.png}")

    if args.react:
        jsx = to_react_component(svg, component_name="VectorAsset")
        with open(args.react, "w", encoding="utf-8") as f:
            f.write(jsx)
        print(f"Exported React Component: {args.react}")

if __name__ == "__main__":
    main()
