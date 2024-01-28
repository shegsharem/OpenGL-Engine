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
        self.vtx_buff_obj = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program('default')

    def get_vertex_array_object(self):
        """Associate vertex buffer object with shader program 

        :return: vertex array object
        :rtype: _type_
        """
        vtx_array_obj = self.context.vertex_array(
            self.shader_program,[(self.vtx_buff_obj,'3f','in_position')])
        return vtx_array_obj

    def get_vertex_data(self) -> np.ndarray:
        """Convert vertex data to numpy array

        :return: `vertex data array`
        :rtype: np.array
        """
        vertex_data = [(-0.6,-0.8,0.0),(0.6,-0.8,0.0),(0.0,0.8,0.0)]
        vertex_data = np.array(vertex_data,dtype='f4')
        return vertex_data

    def get_vertex_buffer_object(self):
        """Send vertex data to GPU memory

        :return: vertex buffer
        :rtype: `buffer` object
        """
        vertex_data = self.get_vertex_data()
        vtx_buff_obj = self.context.buffer(vertex_data)
        return vtx_buff_obj

    def get_shader_program(self, shader_name:str):
        """Prepare shader for compiling

        :param shader_name: name of shader
        :type shader_name: str
        :return: _description_
        :rtype: _type_
        """
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.context.program(
            vertex_shader   = vertex_shader,
            fragment_shader = fragment_shader)

        return program
