'''import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Vertices del cubo
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Edges del cubo
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

# Dibuja el cubo
def draw_cube():
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Dibuja el plano (cuadrado)
def draw_plane():
    glColor3f(1.0,1.0,1.0)
    glBegin(GL_QUADS)
    glVertex3f(-5, -1, -5)
    glVertex3f(-5, -1, 5)
    glVertex3f(5, -1, 5)
    glVertex3f(5, -1, -5)
    glEnd()

# Función principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    # Posición inicial del cubo
    cube_x, cube_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Captura de teclas para mover el cubo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cube_x -= 0.1
        if keys[pygame.K_RIGHT]:
            cube_x += 0.1
        if keys[pygame.K_UP]:
            cube_y += 0.1
        if keys[pygame.K_DOWN]:
            cube_y -= 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibuja el plano
        draw_plane()

        glPushMatrix()
        # Traslada el cubo a su nueva posición
        glTranslatef(cube_x, cube_y, 0.0)
        # Dibuja el cubo
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()'''

#################################################3

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

verticies = [
    [1, 0, -1],
    [1, 0.5, -1],
    [-1, 0.5, -1],
    [-1, 0, -1],
    [1, 0, 1],
    [1, 1, 1],
    [-1, 0, 1],
    [-1, 1, 1]
]

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
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

cube_speed = 0.20
grid_size = 120
grid_spacing = 1
rotation_angle = 0.0

def draw_grid():
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)
    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)
    glEnd()

def Cube():
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def rotate_cube(angle):
    glPushMatrix()
    glLoadIdentity()
    glRotatef(angle, 0, 1, 0)
    glMultMatrixf(np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]], dtype=np.float32))
    modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
    glPopMatrix()
    glMultMatrixf(modelview)

def main():
    global rotation_angle
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    #gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20.0)
    glRotatef(7, 1, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rotation_angle += 90.0
                elif event.key == pygame.K_LEFT:
                    rotation_angle -= 90.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        rotate_cube(rotation_angle)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
