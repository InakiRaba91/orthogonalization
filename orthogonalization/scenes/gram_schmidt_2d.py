from tkinter import W
from manim import *

class GramSchmidt2D(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]},
        )
        self.add(axes)                       

        # Write text with explanation inside a rectangle
        steps = [
            r"\text{Base vectors: }\mathbf{v}_1, \mathbf{v}_2",
            r"\text{Normalize }\mathbf{v}_1\text{ to get }\mathbf{w}_1",
            r"\text{Project }\mathbf{v}_2\text{ onto }\mathbf{w}_1\text{ to get }\mathbf{p}",
            r"\text{Subtract the projection from }\mathbf{v}_2",
            r"\text{Normalize to get }\mathbf{w}_2",
        ]
        texts = [
            MathTex(step, color=WHITE).scale(0.7).to_edge(2*LEFT+2*UP)
            for step in steps
        ]
        # find index for text requiring the widest text box
        idx = max(range(len(texts)), key=lambda i: texts[i].get_width())
        rect = SurroundingRectangle(texts[idx], color=WHITE)

        # Add xy labels
        x_label = Text("x").next_to(axes.x_axis.get_tip(), RIGHT)
        y_label = Text("y").next_to(axes.y_axis.get_tip(), LEFT+0.1*DOWN)
        self.add(x_label, y_label)

        # Draw vectors
        p1 = (-1.5, 2)
        p2 = (0.5, 3)
        v1 = Vector(direction=axes.c2p(*p1), color=RED)
        v2 = Vector(direction=axes.c2p(*p2), color=BLUE)
        v1_label = MathTex(r"\mathbf{v}_1", color=RED).next_to(v1, 0.5*LEFT+0.3*UP)
        v2_label = MathTex(r"\mathbf{v}_2", color=BLUE).next_to(v2, 0.8*UP+0.2*RIGHT)
        self.play(Create(v1), Create(v2), Write(v1_label), Write(v2_label), Create(rect), Write(texts[0]), run_time=2)
        self.wait(1)

        # Normalize v1
        w1 = Vector(direction=axes.c2p(*normalize(p1)), color=YELLOW).set_stroke(width=10)
        v1_transformed = v1.copy()
        w1_label = MathTex(r"\mathbf{w}_1", color=YELLOW).next_to(w1, UP)
        self.play(FadeOut(texts[0]))
        self.play(Transform(v1_transformed, w1), Write(texts[1]), run_time=3)
        self.play(Write(w1_label))
        self.wait(1)

        # Projection of v1 onto v2
        proj = np.dot(p2, normalize(p1)) * normalize(p1)
        p3 = p2 - proj
        proj_vector = Vector(direction=axes.c2p(*proj), color=PURPLE)
        proj_label = MathTex(r"\text{p}", color=PURPLE).next_to(proj_vector, 0.2*LEFT)
        orth_proj_vector = DashedLine(start=axes.c2p(*proj), end=axes.c2p(*p2), color=WHITE)
        self.play(FadeOut(texts[1]))

        # Right angle elbow

        # line1 = Line( ORIGIN, RIGHT )
        # line2 = Line( DOWN, UP )
        # rightangle = RightAngle(line1, line2)
        # self.add(line1, line2, rightangle)

        right_angle = RightAngle(orth_proj_vector, proj_vector, length=0.4, stroke_width=2, quadrant=(1, -1))
        self.play(Create(VGroup(orth_proj_vector, right_angle)), Write(texts[2]), run_time=3)
        self.play(Create(proj_vector),  Write(proj_label), run_time=3)
        self.wait(1)

        # Draw the orthogonal component of v2
        w2_long = Vector(direction=axes.c2p(*p3), color=YELLOW).set_stroke(width=10)
        v2_transformed = v2.copy()
        self.play(FadeOut(texts[2]))
        self.play(Transform(v2_transformed, w2_long), Write(texts[3]), run_time=3)
        self.wait(1)

        # Normalize w2
        w2 = Vector(direction=axes.c2p(*normalize(p3)), color=YELLOW).set_stroke(width=10)
        self.play(FadeOut(texts[3]))
        self.play(Transform(v2_transformed, w2), Write(texts[4]), run_time=3)
        w2_label = MathTex(r"\mathbf{w}_2", color=YELLOW).next_to(w2, RIGHT)
        self.play(Write(w2_label))
        self.wait(2)

# To render the scene, run the following command in your terminal:
# poetry run manimgl orthogonalization/scenes/gram_schmidt_2d.py GramSchmidt2D