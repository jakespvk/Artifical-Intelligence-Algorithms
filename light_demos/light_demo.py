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
    
    screen_width = 2800
    screen_height = 1800
    # For Mac people.
    #pygame.display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 4)
    #pygame.display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 1)
    #pygame.display.gl_set_attribute(GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
    #pygame.display.gl_set_attribute(GL_CONTEXT_PROFILE_COMPATIBILITY, GL_CONTEXT_PROFILE_CORE)
    #pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)

    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("Diffuse lighting demo")

    bunny = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")
    bunny.center_point(glm.vec3(-0.03, 0.07, 0))
    bunny.move(glm.vec3(0.1, -0.5, -3))
    bunny.grow(glm.vec3(5, 5, 5))
    
    # On Mac, we were getting errors when compiling shaders before loading a mesh.
    #mesh_rink = load_textured_obj("models/hockey_rink.obj", "models/rink_pic.jpg")
    mesh_goal = load_textured_obj("models/goal.obj", "models/white.jpg")
    mesh_ice = load_textured_obj("models/cube.obj", "models/rink_pic.jpg")
    #rink = load_textured_obj("models/mini_ice_rink.obj", "models/ice_texture.jpg")
    #mesh = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")
    puck = load_textured_obj("models/puck.obj", "models/black.png")
    mesh_stick = load_textured_obj("models/stick.obj", "models/red.jpg")
    broom = load_textured_obj("models/Broom.obj", "models/white.jpg")

    light = load_textured_obj("models/cube.obj", "models/wall.jpg")
    light.center_point(glm.vec3(0, 0, -10))
    light.move(glm.vec3(0, 0, -1))
    light.grow(glm.vec3(0.01, 0.01, 0.01))

    # Load the vertex and fragment shaders for this program.
    vertex_shader = shaders.compileShader(
        load_shader_source("shaders/normal_perspective.vert"), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source("shaders/specular_light.frag"), GL_FRAGMENT_SHADER
    )
    shader_lighting = shaders.compileProgram(vertex_shader, fragment_shader)

    # Compile a second shader for drawing the "light" cube, which should
    # not light *itself*.
    fragment_shader = shaders.compileShader(
        load_shader_source("shaders/texture_mapped.frag"), GL_FRAGMENT_SHADER
    )
    shader_no_lighting = shaders.compileProgram(vertex_shader, fragment_shader)
    
    renderer = RenderProgram()

    #separate renderer for background
    #vertex_shader2 = shaders.compileShader(
    #        load_shader_source("shaders/textured_perspective.vert"), GL_FRAGMENT_SHADER
    #        )
    #fragment_shader2 = shaders.compileShader(
    #        load_shader_source("shaders/texture_mapped.frag"), GL_FRAGMENT_SHADER
    #        )
    #shader_no_transform = shaders.compileProgram(vertex_shader2, fragment_shader2)
    ##will this work??? in the other one it's:
    ## renderer2 = RenderProgram(shader_no_transform)
    #renderer2 = RenderProgram(shader_no_transform)

    # Define the scene.
    camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )
    

    # Initialize lighting parameters.
    ambient_color = glm.vec3(1, 1, 1)
    ambient_intensity = 0.6
    point_position = glm.vec3(0, 0, 0.01)
    renderer.set_uniform("ambientColor", ambient_color * ambient_intensity, glm.vec3)
    renderer.set_uniform("pointPosition", point_position, glm.vec3)
    renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)
    renderer.set_uniform("viewVector", glm.vec3(0, 0, 0), glm.vec3)

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()

    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    spin = False

    #bunny
    bunny.grow(glm.vec3(1, 1, 3))
    bunny.move(glm.vec3(-0.2, -0.2, 0))
    
    #goal
    mesh_goal.grow(glm.vec3(0.00015, 0.00015, 0.00015))
    mesh_goal.rotate(glm.vec3(0.2, 0, 0))
    mesh_goal.move(glm.vec3(-0.1, -0.04, 0.14))

    #ice
    mesh_ice.grow(glm.vec3(3, 2, 0))
    mesh_ice.move(glm.vec3(-0.2, 0, 0))
    mesh_ice.rotate(glm.vec3(0.1, 0, 0))

    #rink
    #rink.grow(glm.vec3(3, 2, 0))
    #rink.move(glm.vec3(-0.2, 0, -0.5))
    #rink.rotate(glm.vec3(0.1, 0, 0))

    #puck
    puck.grow(glm.vec3(0.0005, 0.0005, 0.0005))
    puck.move(glm.vec3(-0.3, -0.6, 0))
    puck.rotate(glm.vec3(0.4, 0, 0))

    #broom 
    broom.grow(glm.vec3(0.02, 0.02, 0.02))

    #stick
    mesh_stick.grow(glm.vec3(0.01, 0.01, 0.01))
    mesh_stick.move(glm.vec3(-0.1, -0.7, 0))
    mesh_stick.rotate(glm.vec3(-0.7, 0.0, 0))

    SHOT = False
    def shoot_puck():
        for _ in range(19469):
            puck.move(glm.vec3(0, 0.00003, 0))
            puck.grow(glm.vec3(0.9999, 0.9999, 0.9999))

    def shoot_puck_testing():
        for _ in range(19469):
            puck.move(glm.vec3(0, 0.00001, 0))
            puck.grow(glm.vec3(0.9999, 0.9999, 0.9999))


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if (SHOT == False) and (event.key == pygame.K_SPACE):
                    shoot_puck()
                    SHOT = True
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_a in keys_down:
            puck.move(glm.vec3(-0.001, 0, 0))
            mesh_stick.move(glm.vec3(-0.001, 0, 0))
        if pygame.K_d in keys_down:
            puck.move(glm.vec3(0.001, 0, 0))
            mesh_stick.move(glm.vec3(0.001, 0, 0))
        elif pygame.K_l in keys_down:
           light.move(glm.vec3(-0.001, 0, 0))
           renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_h in keys_down:
           light.move(glm.vec3(0.001, 0, 0))
           renderer.set_uniform("pointPosition", light.position, glm.vec3)
        #elif pygame.K_j in keys_down:
        #   light.move(glm.vec3(0, -0.005, 0))
        #   renderer.set_uniform("pointPosition", light.position, glm.vec3)
        #elif pygame.K_k in keys_down:
        #   light.move(glm.vec3(0, 0.005, 0))
        #   renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_SPACE in keys_down:
            spin = not spin

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the bunny with lighting.
        renderer.use_program(shader_lighting)
        renderer.set_uniform("pointPosition", light.get_position(), glm.vec3)
        renderer.render(perspective, camera, [mesh_stick, mesh_goal, puck, mesh_ice])
   
        # Draw the light source without lighting itself.
        renderer.use_program(shader_no_lighting)
        renderer.render(perspective, camera, [light])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        #print(f"{frames/(end - start)} FPS")

    pygame.quit()
