import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

def generate_height_map(size, scale):
    height_map = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            height = math.sin(x * scale) + math.cos(y * scale)  # Efecto ondulado
            height_map[x, y] = height
    return height_map

def generate_terrain(size, scale):
    height_map = generate_height_map(size, scale)
    vertices = []

    for x in range(size - 1):
        for y in range(size - 1):
            # Definir los 6 vértices para cada cuadrado de la malla
            for i, j in [(0, 0), (1, 0), (0, 1), (1, 0), (1, 1), (0, 1)]:
                vx = x + i
                vy = y + j
                vz = height_map[vx, vy]
                vertices.append([vx, vz, vy])

    return np.array(vertices, dtype=np.float32)

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    # Configuración de OpenGL
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad para la correcta visualización de la malla

    # Generar el terreno
    size = 260
    scale = 0.2
    vertices = generate_terrain(size, scale)

    # Crear VBOs (Vertex Buffer Objects)
    VBO = glGenBuffers(1)

    # Vértices
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Vincular atributos de vértices
    glVertexPointer(3, GL_FLOAT, 0, None)
    glEnableClientState(GL_VERTEX_ARRAY)

    # Habilitar el modo wireframe (solo dibujar la malla)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Configuración de la cámara (ajustada para ver todo el terreno)
    gluPerspective(45, (800 / 600), 0.1, 320.0)  # Perspectiva de 45 grados, relación de aspecto, cerca y lejos
    #glTranslatef(-50.0, -10.0, -150.0)  # Mover la cámara hacia atrás y en una posición adecuada
    glTranslatef(-130.0, -10.0, -150)


    # Bucle principal
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        key = pygame.key.get_pressed()

        # TRANSLACIONES
        if key[pygame.K_UP]:
            glTranslatef(0,0,0.5)
        if key[pygame.K_DOWN]:
            glTranslatef(0,0,-0.5)
        if key[pygame.K_RIGHT]:
            glTranslatef(-0.5,0,0)
        if key[pygame.K_LEFT]:
            glTranslatef(0.5,0,0)

        # ROTACIONES
        if key[pygame.K_r]:
            glRotatef(0.05,1.0,0.0,0.0)
        if key[pygame.K_t]:
            glRotatef(-0.05,1.0,0.0,0.0)

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar el terreno (malla)
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
