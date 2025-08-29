#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

grid_size = 140
grid_spacing = 1

def load_obj(filename):
    vertices = []
    edges = []
    surfaces = []
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
                for i in range(len(face_indices)):
                    edges.append((face_indices[i], face_indices[(i + 1) % len(face_indices)]))

    min_v = np.min(vertices, axis=0)
    max_v = np.max(vertices, axis=0)
    center = (min_v + max_v) / 2.0
    vertices = [list(np.array(v) - center) for v in vertices]
    
    return vertices, edges, surfaces

def draw_walls():
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)#################################
    glEnable(GL_POLYGON_OFFSET_FILL)##################################
    glPolygonOffset(1.0, 1.0)
    glLineWidth(1.6)  # Set line width (optional)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,0.0)
    path = r'C:\Users\Usuario\Documents\fondo\maze_large_with_plazes.obj'
    vertices, edges, surfaces = load_obj(path)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glColor3f(0.2,0.5,0.3)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)################################
    glEndList()
    return model_list

def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glBegin(GL_QUADS)
    glColor3f(0.3,0.2,0.4)
    glVertex3f(-grid_size,0,-grid_size)
    glVertex3f(grid_size,0,-grid_size)
    glVertex3f(grid_size, 0, grid_size)
    glVertex3f(-grid_size, 0, grid_size)
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)########### 
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
    
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
    
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(0.0, 0.0, -10)
    
    glEnable(GL_DEPTH_TEST)
    #font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)

    #cube_list = Cube()
    grid_list = draw_grid()
    #other_list = other_cube()
    model_list = draw_walls()
    #hide_data = False

    scale = 1.0
    x = 0
    z = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glScalef(scale,scale,scale)

        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        glPushMatrix()
        glScalef(0.02,0.012,0.02)######################
        glRotatef(90, 1, 0, 0)
        glTranslatef(0.0, 0.0, -17.5)
        glTranslatef(0.0, 1.9, 0.0)
        glScalef(10.0,10.0,10.0)
        glCallList(model_list)
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

        glFlush()
        pygame.display.flip()
        pygame.time.wait(10)

main()
pygame.quit()
