"""
BekVector Spring Physics — Second-Order Elastic Dynamics.
Calculates realistic spring oscillations with stiffness and damping for fluid jelly motion.
"""

import math
from typing import List

class Spring:
    """Second-order spring-damper simulator: F = -k*x - c*v"""
    def __init__(self, stiffness: float = 240.0, damping: float = 18.0, mass: float = 1.0):
        self.k = stiffness
        self.c = damping
        self.m = mass

    def simulate_trajectory(self, start: float, target: float, duration_s: float = 1.0, fps: int = 60) -> List[float]:
        """Simulates position trajectory from start to target over duration."""
        steps = int(duration_s * fps)
        dt = 1.0 / fps
        x = start
        v = 0.0
        trajectory = []

        for _ in range(steps):
            displacement = x - target
            force_spring = -self.k * displacement
            force_damper = -self.c * v
            a = (force_spring + force_damper) / self.m
            v += a * dt
            x += v * dt
            trajectory.append(round(x, 2))

        return trajectory

    def get_value_at(self, t_norm: float, start: float, target: float) -> float:
        """Evaluates closed-form analytical underdamped spring equation at normalized time t in [0, 1]."""
        t = t_norm * 1.5  # scale time window
        omega_0 = math.sqrt(self.k / self.m)
        zeta = self.c / (2 * math.sqrt(self.k * self.m))

        if zeta < 1.0:
            # Underdamped oscillation
            omega_d = omega_0 * math.sqrt(1.0 - zeta * zeta)
            decay = math.exp(-zeta * omega_0 * t)
            coeff = (zeta * omega_0) / omega_d
            val = target - (target - start) * decay * (math.cos(omega_d * t) + coeff * math.sin(omega_d * t))
            return val
        else:
            # Critically damped or overdamped
            decay = math.exp(-omega_0 * t)
            return target - (target - start) * (1.0 + omega_0 * t) * decay
