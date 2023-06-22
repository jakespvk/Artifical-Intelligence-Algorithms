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

        # mat conversion
        local_mat = np.array([local_vertex[0],
                              local_vertex[1],
                              local_vertex[2],
                              1])
        
        # SCALE
        scale_mat = np.array([[self.scale[0], 0, 0, 0],
                              [0, self.scale[1], 0, 0],
                              [0, 0, self.scale[2], 0],
                              [0, 0, 0, 1]])
        local_mat = np.matmul(scale_mat, local_mat)

        # ROTATIONS 
        # yaw
        cos = math.cos(self.orientation[1])
        sin = math.sin(self.orientation[1])

        yaw_mat = np.array([[cos, 0, -sin, 0],
                           [0, 1, 0, 0],
                           [sin, 0, cos, 0],
                           [0, 0, 0, 1]])

        local_mat = np.matmul(yaw_mat, local_mat)

        # pitch
        cos = math.cos(self.orientation[0])
        sin = math.sin(self.orientation[0])

        pitch_mat = np.array([[1, 0, 0, 0],
                             [0, cos, sin, 0],
                             [0, -sin, cos, 0],
                             [0, 0, 0, 1]])

        local_mat = np.matmul(pitch_mat, local_mat)
    
        # roll
        cos = math.cos(self.orientation[2])
        sin = math.sin(self.orientation[2])

        roll_mat = np.array([[cos, sin, 0, 0],
                            [-sin, cos, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        local_mat = np.matmul(roll_mat, local_mat)

        # TRANSLATION
        position_mat = np.array([[1, 0, 0, self.position[0]],
                                 [0, 1, 0, self.position[1]],
                                 [0, 0, 1, self.position[2]],
                                 [0, 0, 0, 1]])

        local_mat = np.matmul(position_mat, local_mat)

        return local_mat

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
        
        # pre-compute R U F vectors
        eye_vec = np.array([camera[0], camera[1], camera[2]]) 
        at_vec = np.array([camera[3], camera[4], camera[5]])
        up_vec = np.array([camera[6], camera[7], camera[8]])
        forward = np.array([eye_vec[0] - at_vec[0],
                            eye_vec[1] - at_vec[1],
                            eye_vec[2] - at_vec[2]])
        forward = forward / np.linalg.norm(forward)
        right = (np.cross(np.array([up_vec[0], up_vec[1], up_vec[2]]), forward))
        right = right / np.linalg.norm(right)

        tx = np.dot(eye_vec, right)
        ty = np.dot(eye_vec, up_vec)
        tz = np.dot(eye_vec, forward)
        #ruf matrix here
        '''ruf_mat = np.array([[right[0], up[0], forward[0], 0],
                            [right[1], up[1], forward[1], 0],
                            [right[2], up[2], forward[2], 0],
                            [tx, ty, tz, 1]])'''

        # transpose??? or how do numpy mats work???????
        ruf_mat_tpose = np.array([[right[0], right[1], right[2], -tx],
                            [up_vec[0], up_vec[1], up_vec[2], -ty],
                            [forward[0], forward[1], forward[2], -tz],
                            [0, 0, 0, 1]])

        return np.matmul(world_vertex, ruf_mat_tpose)

    def view_to_clip(self, view_vertex: np.ndarray, frustum) -> np.ndarray:
        """
        Projects the view-space vertex to clip space (normalized device coordinates).
        """

        # Finish this function to compute (xn, yn, zn) by first projecting
        # to the near-plane coordinates (xp, yp, zp), and then interpolating
        # along the clip space 2x2x2 cube.
        near, far, left, right, bottom, top = frustum

        perspective_projection_mat = np.array([
            [(2 * near) / (right - left), 0, (right + left) / (right - left), 0],
            [0, (2 * near) / (top - bottom), (top + bottom) / (top - bottom), 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]])

        clip_vertex_pre_normalization = np.matmul(perspective_projection_mat, view_vertex)

        w = clip_vertex_pre_normalization[3]
        clip_vertex = np.array([clip_vertex_pre_normalization[0] / w,
                                clip_vertex_pre_normalization[1] / w,
                                clip_vertex_pre_normalization[2] / w])

        return clip_vertex

    def clip_to_screen(
        self, clip_vertex: np.ndarray, surface: pygame.Surface) -> tuple[int, int]:
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
            v_world = self.local_to_world(np.array([v_local[0], v_local[1], v_local[2], 1]))
            v_view = self.world_to_view(v_world, camera)
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
