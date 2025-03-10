import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import os

os.chdir(r'C:\Users\anton\OneDrive\Documentos\files_used')

# Función para generar el mapa de alturas (montañas)
def generate_height_map(size, scale):
    height_map = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            height = math.sin(x * scale) + math.cos(y * scale)  # Efecto ondulado
            height_map[x, y] = height
    return height_map

# Función para generar los vértices del terreno (sin shaders, solo la malla)
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

def load_obj():
    vertices = []
    edges = set()
    filename = 'VideoShip.obj'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                for i in range(len(face_indices)):
                    edges.add(tuple(sorted((face_indices[i], face_indices[(i + 1) % len(face_indices)]))))
    return vertices, edges

# Inicialización de Pygame y OpenGL
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    # Configuración de OpenGL
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad

    # Generar el terreno
    size = 300
    scale = 0.1
    vertices = generate_terrain(size, scale)

    x = -size/2
    y = -5.0
    z = -150.0

    rot = 0.0

    # Cargar el modelo .obj
    model_vertices, edges = load_obj()

    # Crear la lista de visualización para el modelo cargado
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(model_vertices[vertex])
    glEnd()
    glEndList()

    # Crear VBOs (Vertex Buffer Objects) para el terreno
    VBO = glGenBuffers(1)

    # Vértices del terreno
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Vincular atributos de vértices
    glVertexPointer(3, GL_FLOAT, 0, None)
    glEnableClientState(GL_VERTEX_ARRAY)

    # Habilitar el modo wireframe (solo dibujar la malla)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Configuración de la cámara
    gluPerspective(45, (800 / 600), 0.1, 320.0)
    glTranslatef(x, y, z)

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
            #glTranslatef(0,0,0.3)
            z += 0.3
        if key[pygame.K_DOWN]:
            z -= 0.3
            #glTranslatef(0,0,-0.3)
        if key[pygame.K_RIGHT]:
            x -= 0.3
            #glTranslatef(-0.3,0,0)
        if key[pygame.K_LEFT]:
            x += 0.3
            #glTranslatef(0.3,0,0)

        # ROTACIONES
        if key[pygame.K_r]:
            glRotatef(0.05,1.0,0.0,0.0)
        if key[pygame.K_t]:
            glRotatef(-0.05,1.0,0.0,0.0)
        if key[pygame.K_q]:
            glRotatef(-0.05,0.0,1.0,0.0)
        if key[pygame.K_w]:
            glRotate(0.05,0.0,1.0,0.0)

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar el terreno (malla)
        glPushMatrix()
        glColor3f(1.0,1.0,1.0)
        glTranslatef(x, 0, z)
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        glPopMatrix()

        # Dibujar el modelo cargado (sobre el grid)
        glPushMatrix()
        #glTranslatef(-20.0, 0.0, 0.0)  # Ajusta la posición del modelo sobre el terreno si es necesario
        glTranslatef(size/2, 8.0, 120.0)
        glRotatef(-90,0,1,0)
        glRotatef(rot,0,0,1)
        glColor3f(0.0,1.0,0.0)
        glCallList(model_list)
        glPopMatrix()

        #rot += 0.8
        

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
