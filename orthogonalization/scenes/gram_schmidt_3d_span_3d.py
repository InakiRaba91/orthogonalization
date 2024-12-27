from manim import *
from orthogonalization.utils import get_right_angle_elbow


class GramSchmidt3DSpan3D(ThreeDScene):
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
            r"\text{Base vectors: }\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3",
            r"\text{Normalize }\mathbf{v}_1\text{ to get }\mathbf{w}_1",
            r"\text{Project }\mathbf{v}_2\text{ onto }\mathbf{w}_1\text{ to get }\mathbf{p}",
            r"\text{Subtract the projection from }\mathbf{v}_2",
            r"\text{Normalize to get }\mathbf{w}_2",
            r"\text{Project }\mathbf{v}_3\text{ onto span}(\mathbf{w}_1, \mathbf{w}_2)",
            r"\text{Subtract the projection from }\mathbf{v}_3",
            r"\text{Normalize to get }\mathbf{w}_3",
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
        p1 = (-3, 0, 1)
        p2 = (-2, -3, 0.5)
        p3 = (3, 0.5, 4)
        v1 = Vector(direction=axes.c2p(*p1), color=RED)
        v2 = Vector(direction=axes.c2p(*p2), color=BLUE)
        v3 = Vector(direction=axes.c2p(*p3), color=GREEN)
        v1_label = MathTex(r"\mathbf{v}_1", color=RED).to_edge(11*LEFT+5*UP)
        v2_label = MathTex(r"\mathbf{v}_2", color=BLUE).to_edge(8*LEFT+7*UP)
        v3_label = MathTex(r"\mathbf{v}_3", color=GREEN).to_edge(10.5*RIGHT+3.5*UP)
        self.add_fixed_in_frame_mobjects(v1_label, v2_label, v3_label)
        self.play(Create(v1), Create(v2), Create(v3), Write(v1_label), Write(v2_label), Write(v3_label), Create(rect), Write(texts[0]), run_time=2)
        self.wait(1)

        # normalize v1
        q1 = normalize(p1)
        w1 = Vector(direction=axes.c2p(*q1), color=YELLOW).set_stroke(width=10)
        v1_transformed = v1.copy()
        w1_label = MathTex(r"\mathbf{w}_1", color=YELLOW).to_edge(12.7*LEFT+6*UP)
        self.play(FadeOut(texts[0]))
        self.add_fixed_in_frame_mobjects(texts[1])
        self.play(Transform(v1_transformed, w1), Write(texts[1]), run_time=2)
        self.add_fixed_in_frame_mobjects(w1_label)
        self.play(Write(w1_label))
        self.wait(1)

        # projection of v1 onto v2
        proj = np.dot(p2, q1) * q1
        r = p2 - proj
        proj_vector = Vector(direction=axes.c2p(*proj), color=PURPLE)
        orth_proj_vector = Line3D(start=axes.c2p(*proj), end=axes.c2p(*p2), color=WHITE).set_stroke(width=0.5)
        proj_label = MathTex(r"\mathbf{p}", color=PURPLE).scale(0.7).to_edge(12.1*LEFT+7.2*UP)
        self.play(FadeOut(texts[1]))

        #  right angle elbow
        right_angle = get_right_angle_elbow(v1=-proj, v2=r, orig=proj, axes=axes, color=WHITE)
        self.add_fixed_in_frame_mobjects(texts[2])
        orth_group = VGroup(orth_proj_vector, right_angle)
        self.play(Create(orth_group), Write(texts[2]), run_time=2)
        self.add_fixed_in_frame_mobjects(proj_label)
        self.play(Create(proj_vector), Write(proj_label), run_time=2)
        self.wait(1)

        # draw the orthogonal component of v2
        w2_long = Vector(direction=axes.c2p(*r), color=YELLOW).set_stroke(width=10)
        v2_transformed = v2.copy()
        self.play(FadeOut(texts[2]))
        self.add_fixed_in_frame_mobjects(texts[3])
        self.play(Transform(v2_transformed, w2_long), Write(texts[3]), run_time=2)
        self.wait(1)

        # normalize
        q2 = normalize(r)
        w2 = Vector(direction=axes.c2p(*q2), color=YELLOW).set_stroke(width=10)
        self.play(FadeOut(texts[3]))
        self.add_fixed_in_frame_mobjects(texts[4])
        self.play(Transform(v2_transformed, w2), Write(texts[4]), run_time=2)
        w2_label = MathTex(r"\mathbf{w}_2", color=YELLOW).to_edge(12.7*LEFT+9*UP)
        self.add_fixed_in_frame_mobjects(w2_label)
        self.play(Write(w2_label))
        self.wait(2)

        # plane spanned by w1 and w2: nx·x+ny·y+nz·z=0 -> z = -(nx·x+ny·y)/nz
        n = np.cross(q1, q2)
        n = n / np.linalg.norm(n)
        resolution_fa = 1
        plane = Surface(
            lambda u, v: axes.c2p(u, v, -(n[0] * u + n[1] * v) / n[2]),
            resolution=(resolution_fa, resolution_fa),
            u_range=[-4, 4],
            v_range=[-4, 4],
            fill_opacity=0.25,
        )
        plane.set_fill_by_value(axes=axes, colorscale=[ORANGE, ORANGE])
        span_label = MathTex(r"\text{span}(\mathbf{w}_1, \mathbf{w}_2)", color=ORANGE).to_edge(6*RIGHT+2*DOWN)
        self.play(FadeOut(orth_group, proj_vector, proj_label, texts[4]))
        self.add_fixed_in_frame_mobjects(span_label, texts[5])
        self.play(Create(plane), Write(span_label), Write(texts[5]), run_time=2)
        self.wait(1)

        # projection of v3 onto span<v1,v2>
        proj1 = np.dot(p3, q1)
        proj2 = np.dot(p3, q2)
        proj = proj1 * q1 + proj2 * q2
        t = p3 - proj
        proj_vector = Vector(direction=axes.c2p(*proj), color=PURPLE)
        orth_proj_vector = Line3D(start=axes.c2p(*proj), end=axes.c2p(*p3), color=WHITE).set_stroke(width=0.5)
        proj_label = MathTex(r"\mathbf{p}", color=PURPLE).scale(0.7).to_edge(12*RIGHT+9.5*UP)
        self.play(FadeOut(texts[4]))

        #  right angle elbow
        right_angle = get_right_angle_elbow(v1=-proj, v2=t, orig=proj, axes=axes, color=WHITE)
        orth_group = VGroup(orth_proj_vector, right_angle)
        self.play(Create(orth_group), run_time=2)
        self.add_fixed_in_frame_mobjects(proj_label)
        self.play(Create(proj_vector), Write(proj_label), run_time=2)
        self.wait(1)

        # draw the orthogonal component of v2
        w3_long = Vector(direction=axes.c2p(*t), color=YELLOW).set_stroke(width=10)
        v3_transformed = v3.copy()
        self.play(FadeOut(texts[5]))
        self.add_fixed_in_frame_mobjects(texts[6])
        self.play(Transform(v3_transformed, w3_long), Write(texts[6]), run_time=2)
        self.wait(1)

        # normalize
        q3 = normalize(t)
        w3 = Vector(direction=axes.c2p(*q3), color=YELLOW).set_stroke(width=10)
        self.play(FadeOut(texts[6]))
        self.add_fixed_in_frame_mobjects(texts[7])
        self.play(Transform(v3_transformed, w3), Write(texts[7]), run_time=2)
        w3_label = MathTex(r"\mathbf{w}_3", color=YELLOW).to_edge(12.7*RIGHT+5.8*UP)
        self.add_fixed_in_frame_mobjects(w3_label)
        self.play(Write(w3_label))
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manimgl gram_schmidt_2d_span.py GramSchmidt2DSpan