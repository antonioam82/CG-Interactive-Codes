import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
import numpy as np

pygame.init()
pygame.display.set_mode((600, 600), DOUBLEBUF | OPENGL)

# 4 vértices (x, y, z) en float32
vertices = np.array([
    -0.5, -0.5, 0.0,   # 0
     0.5, -0.5, 0.0,   # 1
     0.5,  0.5, 0.0,   # 2
    -0.5,  0.5, 0.0,   # 3
], dtype=np.float32)

# 2 triángulos que reutilizan los vértices anteriores
indices = np.array([0, 1, 2,
                    0, 2, 3], dtype=np.uint32)

# --- Se hace UNA vez: subir los datos a la GPU ---
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.7, 0.2)

    # --- Se hace en CADA frame: una sola llamada de dibujo ---
    glEnableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)          # 3 floats por vértice, desde el inicio del VBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glDisableClientState(GL_VERTEX_ARRAY)

    pygame.display.flip()

glDeleteBuffers(2, [vbo, ebo])
pygame.quit()
