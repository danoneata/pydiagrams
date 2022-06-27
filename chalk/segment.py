import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

from planar import Point, Vec2
from planar.py import Ray

from chalk.trace import Trace


@dataclass
class Segment:
    p: Point
    q: Point

    def get_trace(self) -> Trace:
        def f(point: Point, direction: Vec2) -> List[float]:
            ray = Ray(point, direction)
            inter = sorted(line_segment(ray, self))
            return inter

        return Trace(f)

    def to_ray(self) -> "Ray":
        return Ray(self.p, self.q - self.p)


def ray_ray_intersection(
    ray1: Ray, ray2: Ray
) -> Optional[Tuple[float, float]]:
    """Given two rays

    ray₁ = λ t . p₁ + t v₁
    ray₂ = λ t . p₂ +o t v₂

    the function returns the parameters t₁ and t₂ at which the two rays meet,
    that is:

    ray₁ t₁ = ray₂ t₂

    """
    u = ray2.anchor - ray1.anchor
    x1 = ray1.direction.cross(ray2.direction)
    x2 = u.cross(ray1.direction)
    x3 = u.cross(ray2.direction)
    if x1 == 0 and x2 != 0:
        # parallel
        return None
    else:
        # intersecting or collinear
        return x3 / x1, x2 / x1


def line_segment(ray: Ray, segment: Segment) -> List[float]:
    """Given a line and a segment, return the parameter t for which the line
    meets the segment, that is:

    line t = line t', with t' ∈ [0, 1]

    """
    ray_s = segment.to_ray()
    t = ray_ray_intersection(ray, ray_s)
    if not t:
        return []
    else:
        t1, t2 = t
        if 0 <= t2 <= 1:
            # p = line_s.p + t2 * line_s.v
            return [t1]
        else:
            return []


def ray_circle_intersection(ray: Ray, circle_radius: float) -> List[float]:
    """Given a ray and a circle centered at the origin, return the parameter t
    where the ray meets the circle, that is:

    ray t = circle θ

    The above equation is solved as follows:

    x + t v_x = r sin θ
    y + t v_y = r cos θ

    By squaring the equations and adding them we get

    (x + t v_x)² + (y + t v_y)² = r²,

    which is equivalent to the following equation:

    (v_x² + v_y²) t² + 2 (x v_x + y v_y) t + (x² + y² - r²) = 0

    This is a quadratic equation, whose solutions are well known.

    """
    p = ray.anchor

    a = ray.direction.length2
    b = 2 * (p.dot(ray.direction))
    c = p.length2 - circle_radius**2

    Δ = b**2 - 4 * a * c
    eps = 1e-6  # rounding error tolerance

    if Δ < -eps:
        # no intersection
        return []
    elif -eps <= Δ < eps:
        # tagent
        return [-b / (2 * a)]
    else:
        # the ray intersects at two points
        return [
            (-b - math.sqrt(Δ)) / (2 * a),
            (-b + math.sqrt(Δ)) / (2 * a),
        ]
