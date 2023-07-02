VERTEX_SHADER = shaders.compileShader(
        #version 120
    void main() {
        gl_Position = gl_Vertex;
    },
        GL_VERTEX_SHADER,
    )
