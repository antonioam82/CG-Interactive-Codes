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
    glNewList(model_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)
    glLineWidth(1.6)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,0.0)
    path = r'C:\Users\anton\Downloads\maze_large_with_plazes.obj'
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
    glDisable(GL_POLYGON_OFFSET_FILL)
    glEndList()
    return model_list

def draw_grid(y_offset=0):
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)

    # Plano base
    glBegin(GL_QUADS)
    glColor3f(0.3,0.2,0.4)
    glVertex3f(-grid_size, y_offset, -grid_size)
    glVertex3f(grid_size, y_offset, -grid_size)
    glVertex3f(grid_size, y_offset, grid_size)
    glVertex3f(-grid_size, y_offset, grid_size)
    glEnd()

    glDisable(GL_POLYGON_OFFSET_FILL)
    glLineWidth(1.3)

    # Líneas de cuadrícula
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, y_offset, -grid_size)
        glVertex3f(x, y_offset, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, y_offset, z)
        glVertex3f(grid_size, y_offset, z)
        
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
    glRotatef(15, 1, 0, 0)

    # Listas de dibujo
    floor_grid = draw_grid(0)     # Piso
    ceiling_grid = draw_grid(3)  # Techo
    model_list = draw_walls()

    scale = 1.0
    x = 0
    z = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        key = pygame.key.get_pressed()

        # Controles de movimiento
        if key[pygame.K_UP]:
            glTranslatef(0.0,.0,0.2)
        elif key[pygame.K_DOWN]:
            glTranslatef(0.0,.0,-0.2)
        elif key[pygame.K_LEFT]:
            glTranslatef(0.2,.0,0.0)
        elif key[pygame.K_RIGHT]:
            glTranslatef(-0.2,.0,0.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glScalef(scale,scale,scale)

        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(floor_grid)    # piso
        glCallList(ceiling_grid)  # techo

        glPushMatrix()
        glScalef(0.3,0.09,0.3)
        glRotatef(90, 1, 0, 0)
        glTranslatef(0.0, 0.0, -17.5)
        glTranslatef(0.0, 1.9, 0.0)
        glScalef(20.0,20.0,20.0)
        glCallList(model_list)
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()

        glFlush()
        pygame.display.flip()
        pygame.time.wait(10)

main()
pygame.quit()
