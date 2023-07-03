import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D_normals_done import *
from Object3D_animated import *
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


def get_program(vertex_source_filename, fragment_source_filename):
    vertex_shader = shaders.compileShader(
        load_shader_source(vertex_source_filename), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source(fragment_source_filename), GL_FRAGMENT_SHADER
    )
    return shaders.compileProgram(vertex_shader, fragment_shader)

if __name__ == "__main__":
    pygame.init()
    
    screen_width = 800
    screen_height = 800
    # For Mac people.
    # pygame.display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
    # pygame.display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
    # pygame.display.gl_set_attribute(GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
    # pygame.display.gl_set_attribute(GL_CONTEXT_PROFILE_COMPATIBILITY, GL_CONTEXT_PROFILE_CORE)
    
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")


    #mesh = load_textured_obj("models/dice.obj", "models/dice.png")
    head = load_textured_obj("models/cube.obj", "models/wall.jpg")
    head.move(glm.vec3(0, 0.5, -1))
    head.grow(glm.vec3(0.5, 0.5, 0.5))

    body = Object3D(head.mesh)
    body.move(glm.vec3(0, -1, 0))
    body.grow(glm.vec3(1.5, 1.9,1.5))

    left_arm = Object3D(body.mesh)
    left_arm.move(glm.vec3(-0.6, 0, 0))
    left_arm.grow(glm.vec3(0.3, 1.2, 0.3))
    left_arm.center_point(glm.vec3(0, 0.4, 0))

    head.add_child(body)
    body.add_child(left_arm)

    light = load_textured_obj("models/cube.obj", "models/wall.jpg")
    light.center_point(glm.vec3(0, 0, -1))
    light.move(glm.vec3(0, 0, 1))
    light.grow(glm.vec3(0.01, 0.01, 0.01))

    # Load the vertex and fragment shaders for this program.
    shader_lighting = get_program(
        "shaders/normal_perspective.vert", "shaders/specular_light.frag"
    )
    shader_nolighting = get_program(
        "shaders/normal_perspective.vert", "shaders/texture_mapped.frag"
    )

    renderer = RenderProgram()

    # Define the scene.
    camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )
    

    ambient_color = glm.vec3(1, 1, 1)
    ambient_intensity = 0.1
    point_position = glm.vec3(0, 0, 0)
    renderer.set_uniform("ambientColor", ambient_color * ambient_intensity, glm.vec3)
    renderer.set_uniform("pointPosition", point_position, glm.vec3)
    renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)
    renderer.set_uniform("viewPos", glm.vec3(0, 0, 0), glm.vec3)

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
            head.rotate(glm.vec3(-0.001, 0, 0))
        elif pygame.K_DOWN in keys_down:
            head.rotate(glm.vec3(0.001, 0, 0))
        if pygame.K_RIGHT in keys_down:
            head.rotate(glm.vec3(0, 0.001, 0))
        elif pygame.K_LEFT in keys_down:
            head.rotate(glm.vec3(0, -0.001, 0))
        elif pygame.K_q in keys_down:
            body.rotate(glm.vec3(0.01, 0, 0))
        elif pygame.K_e in keys_down:
            left_arm.rotate(glm.vec3(0.001, 0, 0))
        elif pygame.K_a in keys_down:
           light.move(glm.vec3(-0.001, 0, 0))
           renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_d in keys_down:
           light.move(glm.vec3(0.001, 0, 0))
           renderer.set_uniform("pointPosition", light.position, glm.vec3)
       

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        renderer.use_program(shader_lighting)
        renderer.set_uniform("material", glm.vec4(1, 0.5, 0.9, 16.0), glm.vec4)
        renderer.set_uniform("pointPosition", light.get_position(), glm.vec3)
        renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)
        renderer.render(perspective, camera, [head])

        renderer.use_program(shader_nolighting)
        renderer.render(perspective, camera, [light])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        #print(f"{frames/(end - start)} FPS")

    pygame.quit()
