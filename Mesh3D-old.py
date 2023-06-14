from OpenGL.GL import *
import pygame

# This code is reorganized somewhat from the reading, so we can
# add colors to each of the faces.
class Mesh3D:
    def __init__(
        self,
        vertices: list[tuple[float, float, float]],
        faces: list[tuple[int, int, int, pygame.Color]],
    ):
        self.vertices = vertices
        self.faces = faces

    def draw(self):
        for t in self.faces:
            a, b, c, color = t
            glBegin(GL_LINE_LOOP)
            glColor3ub(color.r, color.g, color.b)
            glVertex3fv(self.vertices[a])
            glVertex3fv(self.vertices[b])
            glVertex3fv(self.vertices[c])
            glEnd()

    # I HATE the way the book creates squares and cubes.
    # A cube is not a DERIVED TYPE of a Mesh3D; it is an *instance*
    # of that class. So we add static helper methods to aid in constructing
    # these simple shapes. 
    @staticmethod
    def square():
        white = pygame.Color(255, 255, 255)
        return Mesh3D(
            [
                (0.5, -0.5, 0.5),
                (-0.5, -0.5, 0.5),
                (0.5, 0.5, 0.5),
                (-0.5, 0.5, 0.5),
                (0.5, 0.5, -0.5),
                (-0.5, 0.5, -0.5),
            ],
            [(0, 2, 3, white), (0, 3, 1, white)],
        )
    
    @staticmethod
    def cube():
        verts = [
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, -0.5, 0.5),
        ]
        tris = [
            (0, 1, 2, pygame.Color(255, 0, 0)),
            (0, 2, 3, pygame.Color(127, 0, 0)),
            (4, 0, 3, pygame.Color(0, 255, 0)),
            (4, 3, 7, pygame.Color(0, 127, 0)),
            (5, 4, 7, pygame.Color(0, 0, 255)),
            (5, 7, 6, pygame.Color(0, 0, 127)),
            (1, 5, 6, pygame.Color(255, 255, 0)),
            (1, 6, 2, pygame.Color(127, 127, 0)),
            (4, 5, 1, pygame.Color(255, 0, 255)),
            (4, 1, 0, pygame.Color(127, 0, 127)),
            (2, 6, 7, pygame.Color(0, 255, 255)),
            (2, 7, 3, pygame.Color(0, 127, 127)),
            
        ]

        return Mesh3D(verts, tris)
