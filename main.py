"""
Generic OpenGL graphics engine
Python 3.12.1
"""
import sys
import pygame
import moderngl as gl

class Engine:
    """Graphics Engine"""
    def __init__(self, screensize=(1600,900)) -> None:
        pygame.init()
        self.screensize = screensize
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)
        # Create OpenGL context
        pygame.display.set_mode(self.screensize,flags=pygame.OPENGL | pygame.GL_DOUBLEBUFFER)

        self.context = gl.create_context()
        self.clock = pygame.time.Clock()

    def check_events(self) -> None:
        """Check input events"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def render(self) -> None:
        """Clear framebuffer and swap buffers"""
        self.context.clear(color=(0.08,0.16,0.18))
        pygame.display.flip()

    def run(self) -> None:
        """Main logic loop"""
        while 1:
            self.check_events()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    engine = Engine()
    engine.run()