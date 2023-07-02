import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D import *
from Object3D import *
from OpenGL.arrays import vbo
from numpy import array
from OpenGL.GL import shaders

import time


def load_obj(filename) -> Object3D:
    with open(filename) as f:
        return Object3D(Mesh3D.load_obj(f))

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # A vertex shader is called on each local-space vertex of a mesh.
    # This basic shader doesn't transform the local coordinate at all;
    # so the clip space coordinate of the vertex matches its local space.
    vertex_shader = open('no_transform.vert', 'r')
    
    VERTEX_SHADER = vertex_shader.read()
    # A fragment shader is called on each pixel that belongs to a 
    # mesh. We are drawing in wireframe mode (see below), so each fragment
    # will be on the edge of one of the triangles of the mesh. Without wireframe 
    # mode, each fragment will be in the interior of one of the triangles.
    fragment_shader = open('all_green.frag', 'r')

    FRAGMENT_SHADER = fragment_shader.read()

    shader_no_transform = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
    shaders.glUseProgram(shader_no_transform)

    # Define the scene.
    mesh = Mesh3D.cube()

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()
    shaders.glUseProgram(shader_no_transform)
    # Only draw wireframes.
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        mesh.draw()

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        print(f"{frames/(end - start)} FPS")

    pygame.quit()
