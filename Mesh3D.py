from OpenGL.GL import *

class Mesh3D:

  def __init__(self):

    self.vertices = [
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5)
            ]

    self.triangles = [0, 2, 3, 0, 3, 1]

  def draw(self):

    for t in range(0, len(self.triangles), 3):

          glBegin(GL_LINE_LOOP)
          glVertex3fv(self.vertices[self.triangles[t]])
          glVertex3fv(self.vertices[self.triangles[t + 1]])
          glVertex3fv(self.vertices[self.triangles[t + 2]])
          glEnd()
