import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D import *
from Object3D import *

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        # Take note of the next line, which informs pygame
        # that OpenGL will do the drawing.
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # Set up OpenGL
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, screen_width / screen_height, 0.1, 100)

    # left, right, bottom, top, near, far
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
    
    # Define the scene.
    mesh = Mesh3D.cube()
    cube = Object3D(mesh)
    cube.position = pygame.Vector3(0, 0, -5)
    # Loop
    done = False
    angle = 0
    scale = 1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear the screen to all black.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube.orientation = pygame.Vector3(angle, 0, 0)
        cube.scale = pygame.Vector3(scale, scale, scale)
        angle += 0.01
        scale += 0.0001
        cube.draw()

        pygame.display.flip()
    pygame.quit()
