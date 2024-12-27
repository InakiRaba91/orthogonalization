
from manim import *

from orthogonalization.utils import get_right_angle_elbow


class GramSchmidt2DSpan3D(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )
        self.add(axes)

        # Write text with explanation inside a rectangle
        steps = [
            r"\text{Base vectors: }\mathbf{v}_1, \mathbf{v}_2",
            r"\text{They span a 2D plane}",
            r"\text{Normalize }\mathbf{v}_1\text{ to get }\mathbf{w}_1",
            r"\text{Project }\mathbf{v}_2\text{ onto }\mathbf{w}_1\text{ to get }\mathbf{p}",
            r"\text{Subtract the projection from }\mathbf{v}_2",
            r"\text{Normalize to get }\mathbf{w}_2",
        ]
        texts = [
            MathTex(step, color=WHITE).scale(0.7).to_edge(3 * UP + 0.5 * LEFT)
            for step in steps
        ]
        # find index for text requiring the widest text box
        idx = max(range(len(texts)), key=lambda i: texts[i].get_width())
        rect = SurroundingRectangle(texts[idx], color=WHITE)
        self.add_fixed_in_frame_mobjects(rect, texts[0])

        # add xyz labels
        x_label = Text("x").to_edge(5.5*RIGHT+4*DOWN)
        y_label = Text("y").to_edge(7.5*RIGHT+6*UP)
        z_label = Text("z").to_edge(13*RIGHT+0.5*UP)
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        self.add(x_label, y_label, z_label)

        # set camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES, zoom=1.3)

        # # draw vectors
        p1 = (-2, 0, 1)
        p2 = (0, 0.5, 3)
        v1 = Vector(direction=axes.c2p(*p1), color=RED)
        v2 = Vector(direction=axes.c2p(*p2), color=BLUE)
        v1_label = MathTex(r"\mathbf{v}_1", color=RED).to_edge(11*LEFT+5*UP)
        v2_label = MathTex(r"\mathbf{v}_2", color=BLUE).to_edge(12.5*RIGHT+3.5*UP)
        self.add_fixed_in_frame_mobjects(v1_label, v2_label)
        self.play(Create(v1), Create(v2), Write(v1_label), Write(v2_label), Create(rect), Write(texts[0]), run_time=2)
        self.wait(1)

        # # d raw plane spanned by v1 and v2: nx·x+ny·y+nz·z=0 -> z = -(nx·x+ny·y)/nz
        n = np.cross(p1, p2)
        n = n / np.linalg.norm(n)
        resolution_fa = 1
        plane = Surface(
            lambda u, v: axes.c2p(u, v, -(n[0] * u + n[1] * v) / n[2]),
            resolution=(resolution_fa, resolution_fa),
            u_range=[-3.3, 3.3],
            v_range=[-0.5, 0.6],
            fill_opacity=0.25,
        )
        plane.set_fill_by_value(axes=axes, colorscale=[GREEN, GREEN])
        span_label = MathTex(r"\text{span}(\mathbf{v}_1, \mathbf{v}_2)", color=GREEN).to_edge(5*RIGHT+DOWN)
        self.play(FadeOut(texts[0]))
        self.add_fixed_in_frame_mobjects(span_label, texts[1])
        self.play(Create(plane), Write(texts[1]), run_time=2)
        self.wait(1)

        # normalize v1
        q1 = normalize(p1)
        w1 = Vector(direction=axes.c2p(*q1), color=YELLOW).set_stroke(width=10)
        v1_transformed = v1.copy()
        w1_label = MathTex(r"\mathbf{w}_1", color=YELLOW).to_edge(12*LEFT+7.5*UP)
        self.play(FadeOut(texts[1]))
        self.add_fixed_in_frame_mobjects(texts[2])
        self.play(Transform(v1_transformed, w1), Write(texts[2]), run_time=2)
        self.add_fixed_in_frame_mobjects(w1_label)
        self.play(Write(w1_label))
        self.wait(1)


        # projection of v1 onto v2
        proj = np.dot(p2, q1) * q1
        p3 = p2 - proj
        proj_vector = Vector(direction=axes.c2p(*proj), color=PURPLE)
        orth_proj_vector = Line3D(start=axes.c2p(*proj), end=axes.c2p(*p2), color=WHITE).set_stroke(width=0.5)
        proj_label = MathTex(r"\mathbf{p}", color=PURPLE).scale(0.7).to_edge(12.3*LEFT+6.8*UP)
        self.play(FadeOut(texts[2]))

        #  right angle elbow
        right_angle = get_right_angle_elbow(v1=-proj, v2=p3, orig=proj, axes=axes, color=WHITE)
        self.add_fixed_in_frame_mobjects(texts[3])
        self.play(Create(VGroup(orth_proj_vector, right_angle)), Write(texts[3]), run_time=2)
        self.add_fixed_in_frame_mobjects(proj_label)
        self.play(Create(proj_vector), Write(proj_label), run_time=2)
        self.wait(1)

        # draw the orthogonal component of v2
        w2_long = Vector(direction=axes.c2p(*p3), color=YELLOW).set_stroke(width=10)
        v2_transformed = v2.copy()
        self.play(FadeOut(texts[3]))
        self.add_fixed_in_frame_mobjects(texts[4])
        self.play(Transform(v2_transformed, w2_long), Write(texts[4]), run_time=2)
        self.wait(1)

        # normalize
        w2 = Vector(direction=axes.c2p(*normalize(p3)), color=YELLOW).set_stroke(width=10)
        self.play(FadeOut(texts[4]))
        self.add_fixed_in_frame_mobjects(texts[5])
        self.play(Transform(v2_transformed, w2), Write(texts[5]), run_time=2)
        w2_label = MathTex(r"\mathbf{w}_2", color=YELLOW).to_edge(12.5*RIGHT+7.5*UP)
        self.add_fixed_in_frame_mobjects(w2_label)
        self.play(Write(w2_label))
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manimgl gram_schmidt_2d_span.py GramSchmidt2DSpan