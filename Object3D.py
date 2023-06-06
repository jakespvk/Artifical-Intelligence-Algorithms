from OpenGL.GL import *
from Mesh3D import Mesh3D
import pygame
import primitives


# An object in 3D space, with a mesh, position, orientation (yaw/pitch/roll),
# and scale.
class Object3D:
    def __init__(
        self,
        mesh: Mesh3D,
        position: pygame.Vector3 = pygame.Vector3(0.0, 0.0, 0.0),
        orientation: pygame.Vector3 = pygame.Vector3(0.0, 0.0, 0.0),
        scale: pygame.Vector3 = pygame.Vector3(1.0, 1.0, 1.0),
    ):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale

    def local_to_world(self, local_vertex: pygame.Vector3) -> pygame.Vector3:
        """
        Transforms the given local-space vertex to world space,
        by applying the translation, orientation, and scale vectors
        of the Object3D.
        """

        # Finish this function to return a transformed world-space vertex.
        # Remember the correct order of compound transformations:
        # scale; then rotate yaw, rotate pitch, rotate roll; 
        # then translate.
        return local_vertex

    def world_to_view(self, world_vertex) -> pygame.Vector3:
        """
        Transforms the given world-space vertex to view space,
        by translating and rotating the object according to the 
        camera location and vectors.
        """

        # We don't have a movable camera for this demo, so world space
        # is identical to view space.
        return world_vertex

    def view_to_clip(self, view_vertex: pygame.Vector3, frustum) -> pygame.Vector3:
        """
        Projects the view-space vertex to clip space (normalized device coordinates).
        """

        # Finish this function to compute (xn, yn, zn) by first projecting
        # to the near-plane coordinates (xp, yp, zp), and then interpolating
        # along the clip space 2x2x2 cube.
        return view_vertex

    def clip_to_screen(
        self, clip_vertex: pygame.Vector3, surface: pygame.Surface
    ) -> tuple[int, int]:
        """
        Projects the clip-space/NDC coordinate to the screen space represented
        by the given pygame Surface object. 
        """

        # Finish this function to compute (xs, ys). Don't forget that
        # the the positive y-axis goes DOWN in Pygame, but UP in clip space.
        return (int(clip_vertex.x), int(clip_vertex.y))

    def draw(self, surface: pygame.Surface, frustum):
        projected = []
        for v_local in self.mesh.vertices:
            v_world = self.local_to_world(v_local)
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
