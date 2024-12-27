from manim import *

def get_right_angle_elbow(
    v1: tuple[float], 
    v2: tuple[float], 
    orig: tuple[float], 
    axes: ThreeDAxes,
    length: float = 0.4, 
    color: str = WHITE, 
    radius_dot: float = 0.02,
) -> VGroup:
    u1 = normalize(v1) * length
    u2 = normalize(v2) * length
    line1 = Line3D(start=axes.c2p(*(orig + u1)), end=axes.c2p(*(orig + u1 + u2)), color=color)
    line2 = Line3D(start=axes.c2p(*(orig + u2)), end=axes.c2p(*(orig + u1 + u2)), color=color)
    dot = Dot3D(point=axes.c2p(*(orig + (u1 + u2) / 2)), color=color, radius=radius_dot)
    return VGroup(line1, line2, dot)
