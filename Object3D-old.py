from OpenGL.GL import *
from Mesh3D import Mesh3D
import pygame
# An object in 3D space, with a mesh, position, orientation (yaw/pitch/roll), 
# and scale. 
class Object3D:
    def __init__(
        self,
        mesh : Mesh3D,
        position: pygame.Vector3=pygame.Vector3(0.0, 0.0, 0.0),
        orientation: pygame.Vector3=pygame.Vector3(0.0, 0.0, 0.0),
        scale: pygame.Vector3=pygame.Vector3(1.0, 1.0, 1.0),
    ):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale

    def draw(self):
        glPushMatrix()  # make sure these transformations only apply to this object.
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        # Rotate the roll (around z-axis)
        glRotatef(self.orientation[2], 0, 0, 1)
        # Rotate the pitch (around x-axis)
        glRotatef(self.orientation[1], 1, 0, 0)
        # Rotate the yaw (around y-axis)
        glRotatef(self.orientation[0], 0, 1, 0)

        glScalef(self.scale[0], self.scale[1], self.scale[2])
        self.mesh.draw()
        glPopMatrix()
