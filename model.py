"""
Generic OpenGL model
Python 3.12.1

Rendering Pipeline:
Verticies -> Vertex Shader
"""
import numpy as np

class Triangle:
    """Generic triangle class for OpenGL Engine"""
    def __init__(self, engine) -> None:
        self.engine = engine
