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
import random


def load_obj(filename) -> Object3D:
    with open(filename) as f:
        return Object3D(Mesh3D.load_obj(f))


def load_textured_obj(
    filename, texture_filename
) -> Object3D:
    with open(filename) as f:
        return Object3D(
            Mesh3D.load_textured_obj(
                f, pygame.image.load(texture_filename)
            )
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

def get_bouncing_ball(ball_mesh):
    ball = Object3D(ball_mesh)

    ball.grow(glm.vec3(0.3, 0.3, 0.3))
    ball.move(glm.vec3(random.uniform(-2, 2), random.uniform(1, 6), random.uniform(-2, -15)))
    ball.center_point(glm.vec3(0, 2.965254 / 2, 0))
    ball.set_velocity(glm.vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)))
    ball.set_acceleration(glm.vec3(0, -9.8, 0))
    ball.set_angular_velocity(glm.vec3(math.pi * 2, 0, 0))
    ball.set_material(glm.vec4(1, 1, 0.1, 4))
    return ball


def get_rolling_ball(ball_mesh):
    ball = Object3D(ball_mesh)
    ball.grow(glm.vec3(0.3, 0.3, 0.3))
    ball.move(glm.vec3(-2, 0, -10))
    ball.center_point(glm.vec3(0, 2.965254 / 2, 0))
    ball.set_velocity(glm.vec3(1, 0, 0))
    ball.set_angular_velocity(glm.vec3(0, 0, -1))
    # This ball is shiny!
    ball.set_material(glm.vec4(1, 1, 0.9, 64))
    return ball


def get_ground():
    ground = load_textured_obj("models/cube.obj", "models/wall.jpg")
    ground.grow(glm.vec3(10, 0.1, 10))
    ground.move(glm.vec3(0, -0.05, -10))
    ground.set_material(glm.vec4(1, 1, 0.5, 32))
    return ground


def get_light():
    light = load_textured_obj("models/cube.obj", "models/wall.jpg")
    light.center_point(glm.vec3(0, 0, -1))
    light.move(glm.vec3(0, 3, -8))
    light.grow(glm.vec3(0.03, 0.03, 0.03))
    return light


if __name__ == "__main__":
    pygame.init()

    screen_width = 1200
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

    ball_base = load_textured_obj(
        "models/basketball/Basketball ball.obj",
        "models/basketball/Textures/Basketball ball_BaseColor.png",
    )
    bouncer = get_bouncing_ball(ball_base.mesh)
    roller = get_rolling_ball(ball_base.mesh)
    balls = [bouncer, roller]
    #for i in range(10):
    #    balls.append(get_bouncing_ball(ball_base.mesh))
    
    ground = get_ground()
    light = get_light()
    shadow = get_light()
    shadow.grow(glm.vec3(1.5, 1.5, 1.5))

    # Load the vertex and fragment shaders for this program.
    shader_specular = get_program(
        "shaders/normal_perspective.vert", "shaders/specular_light.frag"
    )
    shader_lightmaps = get_program(
        "shaders/normal_perspective.vert", "shaders/light_maps.frag"
    )
    shader_nolighting = get_program(
        "shaders/normal_perspective.vert", "shaders/texture_mapped.frag"
    )

    renderer = RenderProgram()

    # Define the scene.

    # The camera is 2 meters off the ground, at (0, 2, 0).
    camera = glm.lookAt(glm.vec3(0, 2, 0), glm.vec3(0, 2, -1), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )

    ambient_color = glm.vec3(1, 1, 1)
    ambient_intensity = 0.2
    point_position = glm.vec3(0, 0, 0)
    renderer.set_uniform("ambientColor", ambient_color * ambient_intensity, glm.vec3)
    renderer.set_uniform("pointPosition", light.position, glm.vec3)
    renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)
    renderer.set_uniform("viewPos", glm.vec3(0, 0, 0), glm.vec3)

    # Loop
    done = False

    # Only draw wireframes.
    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    play_animation = True
    last_time = time.perf_counter()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_a in keys_down:
            light.move(glm.vec3(-0.003, 0, 0))
            renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_d in keys_down:
            light.move(glm.vec3(0.003, 0, 0))
            renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_w in keys_down:
            light.move(glm.vec3(0, 0, -0.003))
            renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_s in keys_down:
            light.move(glm.vec3(0, 0, 0.003))
            renderer.set_uniform("pointPosition", light.position, glm.vec3)
        elif pygame.K_SPACE in keys_down:
            play_animation = not play_animation

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        now = time.perf_counter()
        tick_amt = now - last_time
        last_time = now

        if play_animation:
            # bouncer is an Object3D with a ball mesh, originally 2m off the ground,
            # with an acceleration vector of (0, -9.8, 0).

            # Back in the main loop, after computing tick_amount
            for b in balls:
                b.tick(tick_amt)

                if b.position.y < 0:
                    b.position.y = 0
                    #b.velocity.y *= -0.8

                    b.velocity *= glm.vec3(0.8, -0.8, 0.8)
                    b.angular_velocity *= 0.8

        shadow.set_position(glm.vec3(light.position.x, 0, light.position.z))

        renderer.use_program(shader_specular)
        renderer.render(perspective, camera, balls)

        renderer.use_program(shader_lightmaps)
        renderer.set_uniform("specularMap", 1, int)
        renderer.render(perspective, camera, [ground])

        renderer.use_program(shader_nolighting)
        renderer.render(perspective, camera, [light, shadow])

        pygame.display.flip()

    pygame.quit()
