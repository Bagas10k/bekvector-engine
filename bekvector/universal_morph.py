"""
bekvector/universal_morph.py - Universal SVG Icon Morphing & Path Interpolation Engine.
Features Arclength Resampling, Rotational Phase Alignment, and Dynamic Transition Velocity.
"""

import math
import os

class TransitionVelocity:
    """
    Mathematical Velocity Profiles for Hyper-Polished UI Motion.
    Converts linear time progress t in [0, 1] into dynamic velocity with
    anticipation, peak velocity bursts, and damped elastic overshoots.
    """

    @staticmethod
    def snappy_spring(t, overshoot=0.08, damping=14):
        """
        Hyper-snappy transition: Rapid acceleration burst with Hooke's law damped bounce.
        """
        p = max(0.0, min(1.0, t))
        if p == 0.0:
            return 0.0
        if p == 1.0:
            return 1.0

        # Anticipation contraction during first 12%
        if p < 0.12:
            return -math.sin(p / 0.12 * math.pi) * 0.025

        # Remap [0.12, 1.0] to [0.0, 1.0]
        adjusted_p = (p - 0.12) / 0.88
        
        # Spring physics: 1 - exp(-damping * p) * cos(frequency * p)
        freq = 3.5 * math.pi
        decay = math.exp(-damping * adjusted_p * 0.4)
        bounce = math.cos(freq * adjusted_p) * decay * overshoot
        
        # Base ease-out power 4 curve
        base = 1.0 - math.pow(1.0 - adjusted_p, 4)
        return min(1.08, max(0.0, base + bounce))

    @staticmethod
    def exponential_burst(t):
        """
        High velocity burst: extremely fast middle phase with smooth deceleration.
        """
        p = max(0.0, min(1.0, t))
        if p < 0.5:
            return math.pow(2, 20 * p - 10) / 2
        else:
            return (2 - math.pow(2, -20 * p + 10)) / 2

    @staticmethod
    def smooth_swift(t):
        """
        Apple / Linear standard: cubic-bezier(0.16, 1, 0.3, 1) approximation.
        """
        p = max(0.0, min(1.0, t))
        return 1.0 - math.pow(1.0 - p, 3.2)

    @classmethod
    def apply_profile(cls, t, profile="snappy_spring"):
        if profile == "snappy_spring":
            return cls.snappy_spring(t)
        elif profile == "exponential_burst":
            return cls.exponential_burst(t)
        elif profile == "smooth_swift":
            return cls.smooth_swift(t)
        else:
            # Fallback to cosine smooth
            return (1.0 - math.cos(t * math.pi)) / 2.0


class UniversalMorph:
    """
    Universal Path Interpolation & Animation Engine.
    Handles any two arbitrary SVG paths, resamples them to identical point budgets,
    aligns rotational phase to prevent twisting, and applies transition velocity profiles.
    """

    CATALOG = {
        "heart": [
            (32, 54), (16, 38), (8, 24), (14, 12), (24, 12), (32, 20),
            (40, 12), (50, 12), (56, 24), (48, 38)
        ],
        "star": [
            (32, 6), (39, 22), (56, 22), (42, 34), (48, 50),
            (32, 40), (16, 50), (22, 34), (8, 22), (25, 22)
        ],
        "circle": [
            (32 + 22 * math.cos(i * 2 * math.pi / 16), 32 + 22 * math.sin(i * 2 * math.pi / 16))
            for i in range(16)
        ],
        "square": [
            (14, 14), (23, 14), (32, 14), (41, 14), (50, 14),
            (50, 23), (50, 32), (50, 41), (50, 50),
            (41, 50), (32, 50), (23, 50), (14, 50),
            (14, 41), (14, 32), (14, 23)
        ],
        "triangle": [
            (32, 10), (38, 20), (44, 30), (50, 40), (56, 50),
            (44, 50), (32, 50), (20, 50), (8, 50),
            (14, 40), (20, 30), (26, 20)
        ],
        "shield": [
            (32, 10), (52, 14), (50, 34), (42, 48), (32, 56),
            (22, 48), (14, 34), (12, 14)
        ],
        "gear": [
            (32 + (24 if (i % 2 == 0) else 18) * math.cos(i * math.pi / 8),
             32 + (24 if (i % 2 == 0) else 18) * math.sin(i * math.pi / 8))
            for i in range(16)
        ],
        "bell": [
            (32, 10), (36, 12), (38, 24), (46, 42), (52, 48),
            (40, 48), (36, 54), (28, 54), (24, 48), (12, 48),
            (18, 42), (26, 24), (28, 12)
        ],
        "lock": [
            (20, 28), (20, 18), (32, 10), (44, 18), (44, 28),
            (52, 28), (52, 54), (12, 54), (12, 28)
        ],
        "search": [
            (28, 12), (40, 18), (44, 28), (38, 40), (28, 44),
            (18, 40), (12, 28), (18, 16), (28, 12),
            (38, 40), (52, 54), (48, 58), (34, 44)
        ],
        "cloud": [
            (20, 46), (14, 42), (12, 34), (18, 26), (26, 26),
            (30, 16), (40, 16), (46, 22), (54, 26), (56, 36),
            (52, 44), (46, 46)
        ],
        "bolt": [
            (36, 6), (18, 30), (30, 30), (24, 58), (46, 26), (34, 26)
        ]
    }

    @classmethod
    def resample_polygon(cls, points, num_samples=64):
        if len(points) < 2:
            return points

        cum_dist = [0.0]
        total_len = 0.0
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            total_len += d
            cum_dist.append(total_len)

        if total_len == 0:
            return [points[0]] * num_samples

        step = total_len / num_samples
        resampled = []
        curr_seg = 0
        for s in range(num_samples):
            target_dist = s * step
            while curr_seg < n and cum_dist[curr_seg + 1] < target_dist:
                curr_seg += 1

            p1 = points[curr_seg % n]
            p2 = points[(curr_seg + 1) % n]
            seg_len = cum_dist[curr_seg + 1] - cum_dist[curr_seg]
            if seg_len > 0:
                frac = (target_dist - cum_dist[curr_seg]) / seg_len
                x = p1[0] + frac * (p2[0] - p1[0])
                y = p1[1] + frac * (p2[1] - p1[1])
            else:
                x, y = p1[0], p1[1]
            resampled.append((x, y))

        return resampled

    @classmethod
    def align_rotation(cls, poly_a, poly_b):
        num_pts = len(poly_a)
        best_shift = 0
        min_cost = float("inf")

        for shift in range(num_pts):
            cost = 0.0
            for i in range(num_pts):
                pa = poly_a[i]
                pb = poly_b[(i + shift) % num_pts]
                cost += (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2
            if cost < min_cost:
                min_cost = cost
                best_shift = shift

        return [poly_b[(i + best_shift) % num_pts] for i in range(num_pts)]

    @classmethod
    def interpolate(cls, poly_a, poly_b, progress):
        t = progress
        result = []
        for i in range(len(poly_a)):
            x = (1.0 - t) * poly_a[i][0] + t * poly_b[i][0]
            y = (1.0 - t) * poly_a[i][1] + t * poly_b[i][1]
            result.append((x, y))
        return result

    @classmethod
    def polygon_to_smooth_path(cls, points):
        n = len(points)
        if n == 0:
            return ""
        if n < 3:
            return f"M {points[0][0]:.1f} {points[0][1]:.1f} L {points[1][0]:.1f} {points[1][1]:.1f} Z"

        path = [f"M {points[0][0]:.1f} {points[0][1]:.1f}"]
        for i in range(n):
            p0 = points[(i - 1) % n]
            p1 = points[i]
            p2 = points[(i + 1) % n]
            p3 = points[(i + 2) % n]

            cp1_x = p1[0] + (p2[0] - p0[0]) / 6.0
            cp1_y = p1[1] + (p2[1] - p0[1]) / 6.0
            cp2_x = p2[0] - (p3[0] - p1[0]) / 6.0
            cp2_y = p2[1] - (p3[1] - p1[1]) / 6.0

            path.append(f"C {cp1_x:.1f} {cp1_y:.1f}, {cp2_x:.1f} {cp2_y:.1f}, {p2[0]:.1f} {p2[1]:.1f}")

        path.append("Z")
        return " ".join(path)

    @classmethod
    def morph_between(cls, name_or_points_a, name_or_points_b, progress, num_samples=64, velocity_profile=None):
        """
        Public API: Morphs between any two icons with optional dynamic velocity profile.
        """
        pts_a = cls.CATALOG[name_or_points_a] if isinstance(name_or_points_a, str) else name_or_points_a
        pts_b = cls.CATALOG[name_or_points_b] if isinstance(name_or_points_b, str) else name_or_points_b

        poly_a = cls.resample_polygon(pts_a, num_samples=num_samples)
        poly_b = cls.resample_polygon(pts_b, num_samples=num_samples)
        aligned_b = cls.align_rotation(poly_a, poly_b)

        # Apply velocity curve if requested
        t_curved = progress
        if velocity_profile:
            t_curved = TransitionVelocity.apply_profile(progress, profile=velocity_profile)

        interp = cls.interpolate(poly_a, aligned_b, t_curved)
        return cls.polygon_to_smooth_path(interp)

    @classmethod
    def generate_universal_stage(cls, morph_pairs=None, width=1200, height=380):
        if morph_pairs is None:
            morph_pairs = [
                ("heart", "star", "#FF4D6D", "#FFD000", "Favorit ➔ Rating"),
                ("shield", "gear", "#49B3FC", "#A0C4FF", "Security ➔ Settings"),
                ("bell", "bolt", "#FA5D29", "#FFD000", "Alert ➔ Quick Action"),
                ("cloud", "search", "#34D399", "#49B3FC", "Cloud Storage ➔ Query"),
            ]

        cards = []
        for i, (icon_a, icon_b, color_a, color_b, label) in enumerate(morph_pairs):
            cx = 40 + i * 285
            cy = 75

            p_0 = cls.morph_between(icon_a, icon_b, 0.0)
            p_50 = cls.morph_between(icon_a, icon_b, 1.0)

            cards.append(f"""
    <g transform="translate({cx}, {cy})">
      <rect width="260" height="260" rx="20" fill="rgba(20, 24, 36, 0.75)" stroke="rgba(255, 255, 255, 0.12)" stroke-width="1.5" />
      <line x1="20" y1="200" x2="240" y2="200" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1" />
      <g transform="translate(130, 105) scale(1.6) translate(-32, -32)">
        <path d="{p_0}" fill="{color_a}" opacity="0.95">
          <animate attributeName="d" 
                   values="{p_0}; {p_50}; {p_0}" 
                   dur="2.4s" 
                   repeatCount="indefinite" 
                   calcMode="spline" 
                   keySplines="0.16 1 0.3 1; 0.16 1 0.3 1" />
          <animate attributeName="fill" 
                   values="{color_a}; {color_b}; {color_a}" 
                   dur="2.4s" 
                   repeatCount="indefinite" />
        </path>
      </g>
      <text x="130" y="224" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700" fill="#EDEDED" text-anchor="middle" letter-spacing="0.08em">
        {icon_a.upper()} ➔ {icon_b.upper()}
      </text>
      <text x="130" y="242" font-family="'Inter', sans-serif" font-size="10.5" font-weight="500" fill="#8892B0" text-anchor="middle">
        {label}
      </text>
    </g>
""")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="universalBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#08090C" />
      <stop offset="50%" stop-color="#121622" />
      <stop offset="100%" stop-color="#08090C" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#universalBg)" />
  <text x="40" y="44" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="#EDEDED" letter-spacing="0.04em">
    BEKVISUAL · UNIVERSAL ICON MORPHING ENGINE
  </text>
  <text x="{width - 40}" y="44" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="600" fill="#FA5D29" text-anchor="end">
    DYNAMIC TRANSITION VELOCITY · SNAPPY 60 FPS
  </text>
  <line x1="40" y1="56" x2="{width - 40}" y2="56" stroke="rgba(255,255,255,0.12)" stroke-width="1.2" />
  {''.join(cards)}
</svg>"""
        return svg
