"""
Unit Tests for BekVector Engine.
"""

import unittest
from bekvector import BekVector, compute_damped_tangent, format_coord

class TestBekVector(unittest.TestCase):
    def test_coordinate_quantization(self):
        self.assertEqual(format_coord(50.0), "50")
        self.assertEqual(format_coord(50.44), "50.4")
        self.assertEqual(format_coord(50.49), "50.5")

    def test_spline_tangent_damping(self):
        # Acute turn should damp tangent
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

if __name__ == "__main__":
    unittest.main()
