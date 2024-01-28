"""
Generic OpenGL model
Python 3.12.1

Rendering Pipeline:
Verticies 
    -> Vertex Shader (uniforms)
    -> Primitive Assembly 
    -> Rasterization 
    -> Fragment Shader (uniforms)
    -> Tests 
    -> Frame Buffer
"""
import numpy as np

class Triangle:
    """Generic triangle class for OpenGL Engine"""
    def __init__(self, engine) -> None:
        self.engine = engine
        self.context = engine.context

    def get_vertex_data(self) -> NDArray[Any]:
        vertex_data = [(-0.6,-0.8,0.0),(0.6,-0.8,0.0),(0.0,0.8,0.0)]
        vertex_data = np.array(vertex_data,dtype='f4')
        return vertex_data

    def get_vertex_buffer_object(self):
        """Send vertex data to GPU memory

        :return: vertex buffer
        :rtype: `buffer` object
        """
        vertex_data = self.get_vertex_data()
        buff_obj = self.context.buffer(vertex_data)
        return buff_obj
    