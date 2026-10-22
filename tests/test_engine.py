"""
Unit Tests for BekVector Engine & Extensions.
"""

import unittest
from bekvector import (
    BekVector, compute_damped_tangent, format_coord,
    DataViz, Spring, get_theme, generate_animated_weather_svg,
    to_react_component, to_vue_component
)

class TestBekVector(unittest.TestCase):
    def test_coordinate_quantization(self):
        self.assertEqual(format_coord(50.0), "50")
        self.assertEqual(format_coord(50.44), "50.4")
        self.assertEqual(format_coord(50.49), "50.5")

    def test_spline_tangent_damping(self):
        tx, ty = compute_damped_tangent((0, 0), (10, 50), (20, 0), base_smooth=0.35)
        self.assertLess(abs(tx), 15.0)
        self.assertLess(abs(ty), 15.0)

    def test_svg_compilation(self):
        v = BekVector(min_padding=16)
        v.circle(50, 50, 40, fill="#FFD166", stroke="#111111", stroke_w=2)
        v.rect(50, 50, 30, 30, fill="#FA5D29")
        svg = v.to_svg(bg="#0B0D13")
        self.assertIn("<svg", svg)
        self.assertIn("viewBox=", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("#FFD166", svg)
        self.assertIn("#FA5D29", svg)

    def test_dataviz_sparkline(self):
        svg = DataViz.sparkline([10, 20, 15, 30, 45], width=200, height=50)
        self.assertIn("<path", svg)
        self.assertIn("<circle", svg)
        self.assertIn('viewBox="0 0 200 50"', svg)

    def test_dataviz_radar(self):
        svg = DataViz.radar_chart({"CPU": 40, "RAM": 60, "DISK": 80}, radius=50)
        self.assertIn("<polygon", svg)
        self.assertIn("CPU", svg)
        self.assertIn("RAM", svg)

    def test_spring_physics(self):
        spring = Spring(stiffness=200, damping=15)
        traj = spring.simulate_trajectory(0.0, 100.0, duration_s=0.5, fps=30)
        self.assertEqual(len(traj), 15)
        self.assertGreater(traj[-1], 80.0)

    def test_theme_system(self):
        t = get_theme("cyber_ember")
        self.assertEqual(t.accent_primary, "#FA5D29")
        self.assertEqual(t.bg, "#0A0B0E")

    def test_react_exporter(self):
        svg = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" stroke-width="2"/></svg>'
        jsx = to_react_component(svg, component_name="TestIcon", typescript=True)
        self.assertIn("export const TestIcon", jsx)
        self.assertIn("strokeWidth=", jsx)

    def test_standalone_weather_anim(self):
        svg = generate_animated_weather_svg("night_sky", 400, 240)
        self.assertIn("@keyframes twinkle", svg)
        self.assertIn("@keyframes driftBack", svg)
        self.assertIn("<circle", svg)

if __name__ == "__main__":
    unittest.main()
