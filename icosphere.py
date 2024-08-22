import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

os.chdir(r'C:\Users\Antonio\Documents\blender')

grid_size = 120
grid_spacing = 1

def create_grid_display_list():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    
    glBegin(GL_LINES)
    glColor3f(0.7, 1.0, 0.4)  # Color verde

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()
    
    glEndList()
    return grid_list

def load_obj(filename):
    vertices = []
    surfaces = []
    edges = []
    
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                surfaces.append(face_indices)
                # Generar aristas a partir de las caras
                for i in range(len(face_indices)):
                    edge = (face_indices[i], face_indices[(i + 1) % len(face_indices)])
                    edges.append(edge)
    
    return vertices, surfaces, edges

def create_model_display_list(vertices, surfaces, edges):
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    
    # Dibuja las superficies del modelo en color azul
    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Dibuja las aristas del modelo en color blanco
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glEndList()
    return model_list

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    rot = 0
    tran = 0
    fall_speed = 0  # Velocidad de caída
    y_pos = 1.0     # Posición inicial en el eje Y
    z_limit = grid_size

    glClearColor(0.5, 0.5, 0.5, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(20, 1, 0, 0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    grid_list = create_grid_display_list()
    vertices, surfaces, edges = load_obj('ico.obj')
    model_list = create_model_display_list(vertices, surfaces, edges)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        key = pygame.key.get_pressed()

        # Rotaciones
        if key[pygame.K_t]:
            glRotatef(0.1, 0, -1, 0)
        if key[pygame.K_r]:
            glRotatef(0.1, 0, 1, 0)
        if key[pygame.K_q]:
            glRotatef(0.1, -1, 0, 0)
        if key[pygame.K_w]:
            glRotatef(0.1, 0, -1, 0)

        # Iniciar la caída al presionar la tecla 'f'
        '''if key[pygame.K_f]:
            fall_speed = 0.1#0.05  

        # LET'S FALL!!
        if tran >= z_limit:
            fall_speed = 0.1

        # Actualizar la posición en Y del modelo
        y_pos -= fall_speed

        # Dibujar la cuadrícula
        glPushMatrix()
        glTranslatef(0.0, 0.0, -tran)
        glCallList(grid_list)
        glPopMatrix()
        
        # Dibujar el modelo con las superficies y aristas
        glPushMatrix()
        glTranslatef(0.0, y_pos, 0.0)
        glRotatef(rot, 1, 0, 0)
        glCallList(model_list)
        glPopMatrix()

        rot += 0.6 * 2
        tran += 0.016 * 2
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
