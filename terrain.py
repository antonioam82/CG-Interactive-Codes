import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import os

os.chdir(r'C:\Users\Usuario\Documents\fondo')

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

    center = size // 2  # Centro del terreno

    for x_offset in range(-center, center - 1):
        for y_offset in range(-center, center - 1):
            x = center + x_offset
            y = center + y_offset
            # Definir los 6 vértices para cada cuadrado de la malla
            for i, j in [(0, 0), (1, 0), (0, 1), (1, 0), (1, 1), (0, 1)]:
                vx = x + i
                vy = y + j
                vz = height_map[vx, vy]
                vertices.append([vx - center, vz, vy - center])  # Centrar la malla en (0, 0)

    return np.array(vertices, dtype=np.float32)


def load_obj():
    vertices = []
    edges = set()
    faces = []
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
                faces.append(face_indices)
                for i in range(len(face_indices)):
                    edges.add(tuple(sorted((face_indices[i], face_indices[(i + 1) % len(face_indices)]))))
    return vertices, edges, faces

# Inicialización de Pygame y OpenGL
def main():
    pygame.init()
    dimensions = (1600, 880)
    pygame.display.set_mode(dimensions, DOUBLEBUF | OPENGL)

    # Configuración de OpenGL
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad

    # Generar el terreno
    size = 200
    scale = 0.1
    
    scl = 1.0
    scl_ship = 0.5
    
    vertices = generate_terrain(size, scale)
    glScalef(scl,scl,scl)

    x = 0.0
    y = -2.0
    z = -20.0

    x_ship = 0.0
    y_ship = 3.6
    z_ship = 0.0

    #scl = 1.0
    fill = False

    orientation = -90
    v_fact = 0.0
    '''x_o = 0.0
    y_o = 1.0
    z_o = 0.0'''
    
    #rot = 0.0

    # Cargar el modelo .obj
    model_vertices, edges, faces = load_obj()

    # Crear la lista de visualización para el modelo cargado
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(model_vertices[vertex])
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.5,0.5,0.5)
    for face in faces:
        for vertex in face:
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
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Configuración de la cámara
    gluPerspective(45, (dimensions[0] / dimensions[1]), 0.1, 90.0)
    glTranslatef(x, y, z)

    # Bucle principal
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    if fill:
                        fill = False
                    else:
                        fill = True
            '''elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    orientation = -90
                elif event.key == pygame.K_RIGHT:
                    orientation = 90
                elif event.key == pygame.K_UP:
                    orientation = 180
                elif event.key == pygame.K_DOWN:
                    orientation = 0'''

        keys = pygame.key.get_pressed()

        # TRANSLACIONES
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            z += 0.3
            x += 0.3
            orientation = -135
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            z += 0.3
            x -= 0.3
            orientation = 135
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            z -= 0.3
            x -= 0.3
            orientation = 45
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            z -= 0.3
            x += 0.3
            orientation = -45
        elif keys[pygame.K_UP]:
            #x_ship -= 0.3
            z += 0.424
            orientation = 180
        elif keys[pygame.K_DOWN]:
            #x_ship += 0.3
            z -= 0.424
            orientation = 0
        elif keys[pygame.K_RIGHT]:
            #z_ship += 0.3
            x -= 0.424
            orientation = 90
        elif keys[pygame.K_LEFT]:
            #z_ship += 0.008
            x += 0.424
            orientation = -90
            
        if keys[pygame.K_y]:
            y_ship += 0.03
            v_fact = -8.7
        elif keys[pygame.K_u]:
            y_ship -= 0.03
            v_fact = 8.7
        else:
            v_fact = 0.0
        if keys[pygame.K_h]:
            x_ship -= 0.03
        elif keys[pygame.K_j]:
            x_ship += 0.03

        # ESCALADO
        if keys[pygame.K_s]:
            scl += 0.002
            scl_ship += 0.002
        elif keys[pygame.K_d]:
            scl -= 0.002
            scl_ship -= 0.002

        # ROTACIONES
        if keys[pygame.K_r]:
            glRotatef(0.3,1.0,0.0,0.0)
        if keys[pygame.K_t]:
            glRotatef(-0.3,1.0,0.0,0.0)
        if keys[pygame.K_q]:
            glRotatef(-0.3,0.0,1.0,0.0)
        if keys[pygame.K_w]:
            glRotatef(0.3,0.0,1.0,0.0)

        if keys[pygame.K_i]:
            glTranslatef(0,0.3,0)

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glScalef(scl,scl,scl)
        

        # Dibujar el modelo cargado (sobre el grid)
        glPushMatrix()
        glRotatef(orientation,0,1,0)
        glRotatef(v_fact,1,0,0)#############################################################
        glColor3f(0.0,1.0,0.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glTranslatef(x_ship, y_ship, z_ship)
        glScalef(scl_ship,scl_ship,scl_ship)
        #glRotatef(rot,0,0,1)
        glCallList(model_list)
        glPopMatrix()

        # Dibujar el terreno (malla)
        glPushMatrix()
        if fill:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(0.4,0.4,1.0)
        glTranslatef(x, -2.0, z)
        glLineWidth(1.0)
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        ######################################################################
        if fill:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)#GL_LINE
            glColor3f(1.0,1.0,1.0)
            #glTranslatef(x, -2.0, z)
            glLineWidth(2.0)
            glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        ####################################################################
        glPopMatrix()
        glPopMatrix()

        #rot += 0.8

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()          

if __name__ == "__main__":
    main()
