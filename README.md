# Orthogonalization via Gram-Schmidt process

Educational repo to illustrate the process of orthogonalization via the Gram-Schmidt process.

Three scenes are included:
- Orthogonalization of two vectors in 2D
- Orthogonalization of two vectors in 3D
- Orthogonalization of three vectors in 3D

In order to generate the visualizations, simply install the package and run the following command:

```bash
poetry install
```

Then you can generate the visualizations by running the following command:

```bash
poetry run manim -pql orthogonalization/scenes/gram_schmidt_2d_span_3d.py GramSchmidt2DSpan3D
```

If you just want to generate the final frame, simply run

```bash
poetry run manim -pql orthogonalization/scenes/gram_schmidt_2d_span_3d.py GramSchmidt2DSpan3D -s
```

