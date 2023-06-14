from OpenGL.GL import *
from Mesh3D import Mesh3D
import math
import numpy as np
import primitives
import pygame


# An object in 3D space, with a mesh, position, orientation (yaw/pitch/roll),
# and scale.
class Object3D:
    def __init__(
        self,
        mesh: Mesh3D,
        position: np.ndarray = np.array([0.0, 0.0, 0.0]),
        orientation: np.ndarray = np.array([0.0, 0.0, 0.0]),
        scale: np.ndarray = np.array([1.0, 1.0, 1.0])
    ):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale

    def local_to_world(self, local_vertex: np.ndarray) -> np.ndarray:
        """
        Transforms the given local-space vertex to world space,
        by applying the translation, orientation, and scale vectors
        of the Object3D.
        """

        # Finish this function to return a transformed world-space vertex.
        # Remember the correct order of compound transformations:
        # scale; then rotate yaw, rotate pitch, rotate roll; 
        # then translate.

        x, y, z = local_vertex

        # SCALE
        x_s = x * self.scale[0]
        y_s = y * self.scale[1]
        z_s = z * self.scale[2]

        # ROTATIONS:
        
        # yaw
        cos = math.cos(self.orientation[1])
        sin = math.sin(self.orientation[1])

        x_y = x_s * cos + z_s * sin
        y_y = y_s
        z_y = z_s * cos - x_s * sin

        # pitch
        cos = math.cos(self.orientation[0])
        sin = math.sin(self.orientation[0])

        x_p = x_y
        y_p = y_y * cos - z_y * sin
        z_p = y_y * sin + z_y * cos

        # roll
        cos = math.cos(self.orientation[2])
        sin = math.sin(self.orientation[2])

        x_r = x_p * cos - y_p * sin
        y_r = x_p * sin + y_p * cos
        z_r = z_p
        
        # TRANSLATION
        x_t = x_r + self.position[0]
        y_t = y_r + self.position[1]
        z_t = z_r + self.position[2]
        
        return pygame.Vector3(x_t, y_t, z_t)

    def world_to_view(self, world_vertex: np.ndarray, 
                      camera: tuple[int, int, int, int, int, int, int, int, int]
                      ) -> np.ndarray:
        """
        Transforms the given world-space vertex to view space,
        by translating and rotating the object according to the 
        camera location and vectors.
        """

        # We don't have a movable camera for this demo, so world space
        # is identical to view space.
        
        #ruf matrix here

        return world_vertex

    def view_to_clip(self, view_vertex: np.ndarray, frustum) -> np.ndarray:
        """
        Projects the view-space vertex to clip space (normalized device coordinates).
        """

        # Finish this function to compute (xn, yn, zn) by first projecting
        # to the near-plane coordinates (xp, yp, zp), and then interpolating
        # along the clip space 2x2x2 cube.
        near, far, left, right, bottom, top = frustum

        xe, ye, ze = view_vertex

        xp = xe * -0.1 / ze # near = -N
        yp = ye * -0.1 / ze # near = -N

        xn = 2 * xp / (right - left)
        yn = 2 * yp / (top - bottom)
        zn = -near

        return pygame.Vector3(xn, yn, zn)

    def clip_to_screen(
        self, clip_vertex: np.ndarray, surface: np.ndarray) -> tuple[int, int]:
        """
        Projects the clip-space/NDC coordinate to the screen space represented
        by the given pygame Surface object. 
        """

        # Finish this function to compute (xs, ys). Don't forget that
        # the the positive y-axis goes DOWN in Pygame, but UP in clip space.

        screen_vertex: tuple[int, int] = (
                int((clip_vertex[0] + 1) / 2 * surface.get_width()), 
                int(surface.get_height() - ((clip_vertex[1] + 1) / 2 * surface.get_height()))
                )

        return ((screen_vertex[0]), (screen_vertex[1]))

    def draw(self, surface: pygame.Surface, frustum,
             camera: tuple[int, int, int, int, int, int, int, int, int]):
        projected = []
        for v_local in self.mesh.vertices:
            v_world = self.local_to_world(v_local) # is this what the instructions mean???
            v_view = self.world_to_view(v_world)
            v_clip = self.view_to_clip(v_view, frustum)
            v_screen = self.clip_to_screen(v_clip, surface)
            projected.append(v_screen)

        for tri in self.mesh.faces:
            a, b, c = (
                projected[tri[0]],
                projected[tri[1]],
                projected[tri[2]],
            )
            primitives.draw_triangle(surface, a, b, c, tri[3])

