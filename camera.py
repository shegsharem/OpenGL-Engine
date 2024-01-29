"""
OpenGL graphics engine camera
Python 3.12.1
"""
import glm
import pygame

FOV = 50 #deg
NEAR = 0.1
FAR = 100
SPEED = 0.01

class Camera:
    """Camera"""
    def __init__(self, engine) -> None:
        self.engine = engine
        self.aspect_ratio = engine.screensize[0] / engine.screensize[1]
        self.position = glm.vec3(2,3,3)
        self.up = glm.vec3(0,1,0) # up vector
        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)
        self.view_matrix = self.get_view_matrix()
        self.proj_matrix = self.get_projection_matrix()
    
    def update(self):
        self.move()
        self.view_matrix = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.engine.delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position += self.forward * velocity
        if keys[pygame.K_s]:
            self.position -= self.forward * velocity
        if keys[pygame.K_a]:
            self.position -= self.right * velocity
        if keys[pygame.K_d]:
            self.position += self.right * velocity
        if keys[pygame.K_q]:
            self.position += self.up *velocity
        if keys[pygame.K_e]:
            self.position -= self.up * velocity

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(FOV),self.aspect_ratio,NEAR,FAR)
    
    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.position, self.position + self.forward, self.up) #(eye,center,up)