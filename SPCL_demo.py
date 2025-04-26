#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

os.chdir(r'C:\Users\Usuario\Documents\fondo')

#SPCL_demo.py en github
#TO DO: Color 4 grid surface

grid_size = 140
grid_spacing = 1

vertices = (
    (2.0, 0.0, -1.0),
    (2.0, 0.2, -1.0),
    (-2.0, 0.2, -1.0),
    (-2.0, 0.0, -1.0),
    (2.0, 0.0, 1.0),
    (2.0, 0.2, 1.0),
    (-2.0, 0.0, 1.0),
    (-2.0, 0.2, 1.0)
)
 
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)
 
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def draw_plattform():
    platt_list = glGenLists(1)
    glNewList(platt_list, GL_COMPILE)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(0.2,0.4,0.3)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.0,0.0,0.0)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glEndList()
    return platt_list

def load_obj():
    vertices = []
    edges = set()
    faces = []
    filename = 'VideoShip.obj'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]),float(parts[3])]
                vertices.append(vertex)
            if line.startswith('f '):
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                faces.append(face_indices)
                for i in range(len(face_indices)):
                    edges.add(tuple(sorted((face_indices[i], face_indices[(i + 1) % len(face_indices)]))))
    return vertices, edges, faces


def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glLineWidth(1.3)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()
    glEndList()
    return grid_list

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
    glTranslatef(0.0,0.0,-10)
    glEnable(GL_DEPTH_TEST)
    glRotatef(15,1,0,0)
    glClearColor(0.3, 0.3, 0.3, 1.0)

    model_vertices, edges, faces = load_obj()

    grid_list = draw_grid()
    platt_list = draw_plattform()
    

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key_button = pygame.key.get_pressed()

        if key_button[pygame.K_r]:
            glRotatef(0.4,0,1,0)
        elif key_button[pygame.K_t]:
            glRotatef(-0.4,0,1,0)
        elif key_button[pygame.K_y]:
            glRotatef(0.4,1,0,0)
        elif key_button[pygame.K_u]:
            glRotatef(-0.4,1,0,0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glCallList(grid_list)
        glCallList(platt_list)

        pygame.display.flip()
        pygame.time.wait(10)

    glDeleteLists(grid_list,1)
    pygame.quit()

if __name__=="__main__":
    main()
        
