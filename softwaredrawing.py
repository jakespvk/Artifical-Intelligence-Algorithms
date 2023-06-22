import pygame
from Mesh3D import Mesh3D
import math
from Object3D_mat import Object3D
import numpy as np

######
# REQUIREMENTS:
# make a file "primitives.py", and copy all your draw_line, draw_triangle, and fill_triangle code there.
# copy the Mesh3D file from the last lesson.

def make_cube():
    return Object3D(Mesh3D.cube())


if __name__ == "__main__":
    pygame.init()
    screen_width = 3840
    screen_height = 2160
    screen = pygame.display.set_mode((screen_width, screen_height))
    done = False
    m = make_cube()
    m.position = np.array([0, 0, -5])

    # Given the vertical half-FOV, compute coordinates of the perspective frustum.
    v_fov = 30
    near = 0.1
    far = 100
    top = math.tan(math.radians(v_fov)) * near
    right = top * screen_width / screen_height
    left = -right
    bottom = -top

    print("Frustum coordinates: near, far, left, right, bottom, top")
    print(near, far, left, right, bottom, top)
    frustum = (near, far, left, right, bottom, top)
    black = pygame.Color(0, 0, 0)

    i: int = 0

    while not done:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if (i < 1000):
            m.scale += np.array([0.001, 0.001, 0.001])
            m.orientation += np.array([0.001, 0.001, 0.001])
            i += 1
        m.position = np.array([0, 0, -20])
        m.draw(screen, frustum, (0, 0, 0, 0, 0, -5, 0, 1, 0))
        pygame.display.flip()
    pygame.quit()
