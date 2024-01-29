"""
Generic OpenGL graphics engine
Python 3.12.1
"""
import sys
import pygame
import moderngl as gl
from model import Cube, Triangle
from camera import Camera

class Engine:
    """Graphics Engine"""
    def __init__(self, screensize=(1290,690)) -> None:
        pygame.init()
        self.screensize = screensize
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(self.screensize,flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.NOFRAME)
        
        # Create OpenGL context
        self.context = gl.create_context()
        #self.context.front_face = 'cw' # set verticies clockwise
        self.context.enable(flags=gl.DEPTH_TEST | gl.CULL_FACE)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0 

        self.camera = Camera(self)
        self.scene = Cube(self)

    def check_events(self) -> None:
        """Check input events"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.scene.destroy()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene.destroy()
                    pygame.quit()
                    sys.exit()

    def render(self) -> None:
        """Clear framebuffer and swap buffers"""
        self.context.clear(color=(0.125,0.125,0.125))
        self.scene.render()
        pygame.display.flip()
    
    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    def run(self) -> None:
        """Main logic loop"""
        while 1:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == "__main__":
    engine = Engine()
    engine.run()