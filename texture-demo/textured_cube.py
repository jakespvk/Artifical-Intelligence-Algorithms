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

from RenderProgram import *
import time
import math

def load_obj(filename) -> Object3D:
    with open(filename) as f:
        return Object3D(Mesh3D.load_obj(f))

def load_textured_obj(filename, texture_filename) -> Object3D:
    with open(filename) as f:
        return Object3D(
            Mesh3D.load_textured_obj(f, pygame.image.load(texture_filename))
        )

def load_shader_source(filename):
    with open(filename) as f:
        return f.read()


if __name__ == "__main__":
    pygame.init()
    screen_width = 1800
    screen_height = 900
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # On Mac, we were getting errors when compiling shaders before loading a mesh.
    #mesh_rink = load_textured_obj("models/hockey_rink.obj", "models/rink_pic.jpg")
    mesh_goal = load_textured_obj("models/goal.obj", "models/white.png")
    mesh_ice = load_textured_obj("models/cube.obj", "models/ice.png")
    mesh = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")
    mesh2 = load_textured_obj("models/cube.obj", "models/hockey_backdrop.jpg")

    # Load the vertex and fragment shaders for this program.
    vertex_shader = shaders.compileShader(
        load_shader_source("shaders/textured_perspective.vert"), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source("shaders/texture_mapped.frag"), GL_FRAGMENT_SHADER
    )
    shader_no_transform = shaders.compileProgram(vertex_shader, fragment_shader)

    renderer = RenderProgram(shader_no_transform)

    # Define the scene.
    camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()

    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    
    #bunny
    mesh.grow(glm.vec3(3, 3, 3))
    mesh.move(glm.vec3(-0.2, -0.2, 0))
    
    #goal
    mesh_goal.grow(glm.vec3(0.0005, 0.0005, 0.0005))
    #mesh_goal.rotate(glm.vec3(0, math.pi / 2, 0))
    mesh_goal.move(glm.vec3(0, -0.2, 0))
    
    #rink
    #mesh_rink.grow(glm.vec3(0.001, 0.001, 0.001))

    #ice?
    mesh_ice.rotate(glm.vec3(math.pi, 0, 0))
    mesh_ice.move(glm.vec3(0, -1.5, 0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_w in keys_down:
            mesh.move(glm.vec3(0, 0.001, 0))
        if pygame.K_a in keys_down:
            mesh.move(glm.vec3(-0.001, 0, 0))
        if pygame.K_s in keys_down:
            mesh.move(glm.vec3(0, -0.001, 0))
        if pygame.K_d in keys_down:
            mesh.move(glm.vec3(0.001, 0, 0))
        if pygame.K_UP in keys_down:
            mesh.rotate(glm.vec3(-0.1, 0, 0))
        elif pygame.K_DOWN in keys_down:
            mesh.rotate(glm.vec3(0.1, 0, 0))
        if pygame.K_RIGHT in keys_down:
            mesh.rotate(glm.vec3(0, 0.1, 0))
        elif pygame.K_LEFT in keys_down:
            mesh.rotate(glm.vec3(0, -0.1, 0))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the scene given the perspective and camera matrices.
        renderer.render(perspective, camera, [mesh, mesh_goal, mesh_ice])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        print(f"{frames/(end - start)} FPS")

    pygame.quit()

