from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import ctypes
from OpenGL.arrays import vbo
from numpy import array
sizeOfFloat = ctypes.sizeof(GLfloat)

class Mesh3D:
    """
    Represents a 3D mesh using an OpenGL vertex buffer + attrib array to 
    store the vertices and faces.
    """
    def __init__(
        self,
        vertices : list[list[float]] ,
        faces: list[list[int, int, int]]
    ):
        self.vbo = Mesh3D.get_vbo(vertices)
        self.ebo = Mesh3D.get_ebo(faces)
        self.vcount = len(faces * 3)
        self.fcount = len(faces)

    def draw(self, mode=GL_TRIANGLES):
        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeOfFloat, None)
        glEnableVertexAttribArray(0)

        glVertexPointerf(self.vbo)
        glDrawElements(mode, self.vcount, GL_UNSIGNED_INT, None)
        self.vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
     
    @staticmethod
    def get_ebo(faces):
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)
        return ebo
    
    @staticmethod
    def get_vbo(vertices, usage="GL_STATIC_DRAW"):
        buffer_ref = vbo.VBO(vertices, usage)
        return buffer_ref

    @staticmethod
    def square():
        return Mesh3D(
            array([
                0.5, -0.5, 0.5,
                -0.5, -0.5, 0.5,
                0.5, 0.5, 0.5,
                -0.5, 0.5, 0.5,
                0.5, 0.5, -0.5,
                -0.5, 0.5, -0.5,
            ], dtype='float32'),
            array([[0, 2, 3], [0, 3, 1]], dtype="uint32"),
        )
    
    @staticmethod
    def cube():
       
        verts = [
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
        ]
        tris = [
            [0, 1, 2],
            [0, 2, 3],
            [4, 0, 3],
            [4, 3, 7],
            [5, 4, 7],
            [5, 7, 6],
            [1, 5, 6],
            [1, 6, 2],
            [4, 5, 1],
            [4, 1, 0],
            [2, 6, 7],
            [2, 7, 3]
        ]

        return Mesh3D(array(verts, "float32"), array(tris, 'uint32'))

    @staticmethod
    def load_obj(file) -> "Mesh3D":
        verts = []
        faces = []
        for line in file:
            if line[0] == '#':
                continue
            sp = line.split(' ')
            if line[0] == 'v':
                verts.append([float(sp[1]), float(sp[2]), float(sp[3])])
            elif line[0] == 'f':
                faces.append([int(sp[1])-1, int(sp[2])-1, int(sp[3])-1])
        return Mesh3D(array(verts, dtype="float32"), array(faces, 'uint32'))