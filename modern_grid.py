import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# --- SHADERS ---
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 mvp;
void main() {
    gl_Position = mvp * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 0.8, 1.0, 1.0); // Color cyan
}
"""

# --- FUNCIONES MATEMÁTICAS (Sustituyen a GLM) ---
def perspective(fovy, aspect, near, far):
    f = 1.0 / np.tan(fovy / 2.0)
    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)

def translate(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def create_grid(size=20, step=1):
    vertices = []
    for i in range(-size, size + 1, step):
        vertices.extend([float(i), 0, float(-size), float(i), 0, float(size)])
        vertices.extend([float(-size), 0, float(i), float(size), 0, float(i)])
    return np.array(vertices, dtype=np.float32)

def main():
    if not glfw.init(): return

    window = glfw.create_window(1280, 720, "Grid sin GLM (Numpy)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    grid_vertices = create_grid()
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, grid_vertices.nbytes, grid_vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, None)
    glEnableVertexAttribArray(0)

    # Posición de la cámara
    cam_x, cam_y, cam_z = 0.0, 5.0, 15.0
    mvp_loc = glGetUniformLocation(shader, "mvp")

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Controles
        speed = 0.01
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS: cam_z -= speed
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS: cam_z += speed
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS: cam_x -= speed
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS: cam_x += speed

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        # Construcción de matrices
        proj = perspective(np.radians(45.0), 1280/720, 0.1, 100.0)
        # Una matriz de vista simple (solo traslación inversa)
        view = translate(-cam_x, -cam_y, -cam_z)
        
        # MVP = P * V (en este caso el modelo es la identidad)
        mvp = np.dot(proj, view)

        # OpenGL espera las matrices en formato column-major (transpuestas para Numpy)
        glUniformMatrix4fv(mvp_loc, 1, GL_TRUE, mvp)

        glBindVertexArray(vao)
        glDrawArrays(GL_LINES, 0, len(grid_vertices) // 3)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
