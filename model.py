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
import glm
import pygame


class Triangle:
    """Generic triangle class for OpenGL Engine"""
    def __init__(self, engine) -> None:
        self.engine = engine
        self.context = engine.context
        self.vtx_buff_obj = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program('default')
        self.vtx_array_obj = self.get_vertex_array_object()
        self.on_init()

    def on_init(self) -> None:
        """Pass projection matrix from camera instance to shader"""
        self.shader_program['m-proj'].write(self.engine.camera.m_proj)
        self.shader_program['view_matrix'].write(self.engine.camera.view_matrix)

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
        with open(f'shaders/{shader_name}.vert',encoding='utf-8') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag',encoding='utf-8') as file:
            fragment_shader = file.read()

        program = self.context.program(
            vertex_shader   = vertex_shader,
            fragment_shader = fragment_shader)

        return program

    def render(self) -> None:
        """Render triangle"""
        self.vtx_array_obj.render()

    def destroy(self) -> None:
        """Remove frame buffer from memory"""
        self.vtx_buff_obj.release()
        self.shader_program.release()
        self.vtx_array_obj.release()


class Cube:
    """Generic cube class for OpenGL Engine"""
    def __init__(self, engine) -> None:
        self.engine = engine
        self.context = engine.context
        self.vtx_buff_obj = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program('default')
        self.vtx_array_obj = self.get_vertex_array_object()
        self.model_matrix = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/background.png')
        self.on_init()

    def on_init(self) -> None:
        """Pass data to shader program"""
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['proj_matrix'].write(self.engine.camera.proj_matrix)
        self.shader_program['view_matrix'].write(self.engine.camera.view_matrix)
        self.shader_program['model_matrix'].write(self.model_matrix)
    
    def get_texture(self,path):
        texture = pygame.image.load(path).convert_alpha()
        texture = pygame.transform.flip(texture,False,True)
        texture = self.context.texture(size=texture.get_size(),components=3,
                                       data=pygame.image.tostring(texture,"RGB"))
        return texture
    
    def update(self) -> None:
        """Update cube"""
        model_matrix = glm.rotate(self.model_matrix, self.engine.time*0.5, glm.vec3(0,1,0))
        self.shader_program['model_matrix'].write(model_matrix) # update model matrix in shader
        self.shader_program['view_matrix'].write(self.engine.camera.view_matrix) # update view matrix in shader

    
    def get_model_matrix(self) -> glm.mat4x4:
        """Get 4x4 identity matrix"""
        model_matrix = glm.mat4x4()
        return model_matrix

    def get_vertex_array_object(self):
        """Associate vertex buffer object with shader program 

        :return: vertex array object
        :rtype: _type_
        """
        vtx_array_obj = self.context.vertex_array(
            self.shader_program,[(self.vtx_buff_obj,'2f 3f','in_texcoord_0','in_position')])
        return vtx_array_obj

    def get_vertex_data(self) -> np.ndarray:
        """Convert vertex data to numpy array

        :return: `vertex data array`
        :rtype: np.array
        """
        verticies = [
            (-1,-1, 1),( 1,-1, 1),( 1, 1, 1),(-1, 1, 1),
            (-1, 1,-1),(-1,-1,-1),( 1,-1,-1),( 1, 1,-1)
        ]

        indices = [
            (0,2,3),(0,1,2),
            (1,7,2),(1,6,7),
            (6,5,4),(4,7,6),
            (3,4,5),(3,5,0),
            (3,7,4),(3,2,7),
            (0,6,1),(0,5,6)
        ]

        tex_coord = [(0,0),(1,0),(1,1),(0,1)]

        tex_coord_indices = [
            (0,2,3),(0,1,2),
            (0,2,3),(0,1,2),
            (0,1,2),(2,3,0),
            (2,3,0),(2,0,1),
            (0,2,3),(0,1,2),
            (3,1,2),(3,0,1)
        ]

        vertex_data = self.get_data(verticies,indices)
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data,vertex_data]) # combine texture data and vertex data
        return vertex_data

    @staticmethod
    def get_data(verticies:list,indices:list) -> np.ndarray:
        """Generate vertex data based on verticies and their indices

        :param verticies: `list of verticies`
        :type verticies: list
        :param indices: `list of indices`
        :type indices: list
        :return: vertex data array
        :rtype: np.ndarray
        """
        data = [verticies[ind] for triangle in indices for ind in triangle]
        return np.array(data,dtype='f4')

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
        with open(f'shaders/{shader_name}.vert',encoding='utf-8') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag',encoding='utf-8') as file:
            fragment_shader = file.read()

        program = self.context.program(
            vertex_shader   = vertex_shader,
            fragment_shader = fragment_shader)

        return program

    def render(self) -> None:
        """Render cube"""
        self.update()
        self.vtx_array_obj.render()

    def destroy(self) -> None:
        """Remove frame buffer from memory"""
        self.vtx_buff_obj.release()
        self.shader_program.release()
        self.vtx_array_obj.release()