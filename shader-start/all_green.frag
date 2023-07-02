
    FRAGMENT_SHADER = shaders.compileShader(
    #version 120
    void main() {
        gl_FragColor = vec4(0, 1, 0, 1);
    },
        GL_FRAGMENT_SHADER,
    )
