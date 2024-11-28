import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

os.chdir(r'C:\Users\Usuario\Documents\repositorios\libigl-tutorial-data')

def load_obj(filename):
    vertices = []
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                parts = line.strip().split()
                # Las caras pueden tener más de 3 vértices, por lo tanto tenemos que manejar polígonos
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                for i in range(len(face_indices)):
                    edges.append((face_indices[i], face_indices[(i + 1) % len(face_indices)]))
    return vertices, edges

def create_model_display_list(vertices, edges):
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    
    #glLineStipple(1, 0x0101)
    #glEnable(GL_LINE_STIPPLE)
    glLineWidth(1.0)
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
    scale = 1

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(50, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)
    #glRotatef(20,1,0,0)

    # Cargar y compilar las display lists
    vertices, edges = load_obj('cube.obj')
    model_list = create_model_display_list(vertices, edges)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                '''elif event.key == pygame.K_z:
                    #scale += 0.5
                elif event.key == pygame.K_x:
                    scale -= 0.5'''

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            glRotatef(-0.5,1,0,0)
        if key[pygame.K_DOWN]:
            glRotatef(0.5,1,0,0)
        if key[pygame.K_RIGHT]:
            glRotatef(0.5,0,1,0)
        if key[pygame.K_LEFT]:
            glRotatef(-0.5,0,1,0)

        elif key[pygame.K_z]:
            scale += 0.05
        elif key[pygame.K_x]:
            scale -= 0.05

            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glScalef(scale, scale, scale)
        glCallList(model_list)
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()

