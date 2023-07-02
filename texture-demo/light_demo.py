import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D_normals import *
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
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")
    #mesh = load_textured_obj("models/dice.obj", "models/dice.png")
    mesh = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")
    #mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    mesh.center = glm.vec3(-0.03, 0.06, 0)
    mesh.move(glm.vec3(0, 0, -1))
    mesh.grow(glm.vec3(5, 5, 5))

    light = load_textured_obj("models/cube.obj", "models/wall.jpg")
    light.center = glm.vec3(0, 0, -1)
    light.move(glm.vec3(0, 0, 1))
    light.grow(glm.vec3(0.01, 0.01, 0.01))
    #mesh = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")

    # Load the vertex and fragment shaders for this program.
    vertex_shader = shaders.compileShader(
        load_shader_source("shaders/normal_perspective.vert"), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source("shaders/diffuse_light.frag"), GL_FRAGMENT_SHADER
    )
    shader_lighting = shaders.compileProgram(vertex_shader, fragment_shader)

    # This renderer will keep track of the program and apply uniform values when drawing.
    renderer = RenderProgram(shader_lighting)

    # Define the scene.
    camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )
    # In Classic OpenGL, FOVY is given in degrees. It must be radians in Modern OpenGL.

    

    ambient_color = glm.vec3(1, 1, 1)
    ambient_intensity = 0.30
    point_position = glm.vec3(0, 0, 0)
    renderer.set_uniform("ambientColor", ambient_color * ambient_intensity, glm.vec3)
    renderer.set_uniform("pointPosition", point_position, glm.vec3)
    renderer.set_uniform("pointColor", glm.vec3(1, 1, 0), glm.vec3)

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()

    # Only draw wireframes.
    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    spin = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_UP in keys_down:
            mesh.rotate(glm.vec3(-0.001, 0, 0))
        elif pygame.K_DOWN in keys_down:
            mesh.rotate(glm.vec3(0.001, 0, 0))
        if pygame.K_RIGHT in keys_down:
            mesh.rotate(glm.vec3(0, 0.001, 0))
        elif pygame.K_LEFT in keys_down:
            mesh.rotate(glm.vec3(0, -0.001, 0))
        #elif pygame.K_a in keys_down:
        #    light.move(glm.vec3(-0.001, 0, 0))
        #    renderer.set_uniform("pointPosition", light.position, glm.vec3)
        #elif pygame.K_d in keys_down:
        #    light.move(glm.vec3(0.001, 0, 0))
        elif pygame.K_SPACE in keys_down:
            spin = not spin

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if spin:
            light.rotate(glm.vec3(0, 0.001, 0))
        renderer.set_uniform("pointPosition", light.get_position(), glm.vec3)


        # mesh.rotate(glm.vec3(0.01, 0.01, 0.01))
        # Render the scene given the perspective and camera matrices.
        renderer.set_uniform("pointColor", glm.vec3(1, 1, 0), glm.vec3)
        renderer.render(perspective, camera, [mesh])
        renderer.set_uniform("pointColor", glm.vec3(0, 0, 0), glm.vec3)
        renderer.render(perspective, camera, [light])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        #print(f"{frames/(end - start)} FPS")

    pygame.quit()
