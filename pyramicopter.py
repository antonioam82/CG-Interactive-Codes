#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

grid_size = 120
grid_spacing = 1

vertices = [
    [1, 0.15, -1],  # 0
    [1, 0.15, 1],   # 1
    [-1, 0.15, 1],  # 2
    [-1, 0.15, -1], # 3
    [0, 1.15, 0]    # 4 (vértice superior de la pirámide)
]

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (0, 4),
    (1, 4),
    (2, 4),
    (3, 4)
)

surfaces = (
    (0, 4, 3),
    (1, 4, 0),
    (2, 4, 1),
    (3, 4, 2),
    (0, 3, 2, 1),  # Base triangular
)

def Pyramid():
    glBegin(GL_QUADS)
    glColor3f(1.0,0.0,0.0)
    for surface in surfaces: 
        #x=0
        for vertex in surface:
            #x+=1
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,0.0,)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(vertices[vertex])
    glEnd()

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    
def draw_grid():
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)
    speed_factor = 1
    mv = 0
    mv2 = 0

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    #glOrtho(-2, 2, -2, 2, -10, 25)
    glEnable(GL_DEPTH_TEST)####
    glTranslatef(0.0, -1.5, -8.5)
    glRotatef(7, 1, 0, 0)
    angle = 0
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    speed_factor += 1
                elif event.key == pygame.K_o:
                    speed_factor -= 1

        key = pygame.key.get_pressed()

        if key[pygame.K_g]:
            glRotatef(-0.1, 1, 0, 0)
        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
        if key[pygame.K_LEFT]:
            glTranslatef(0.1, 0, 0)
        if key[pygame.K_RIGHT]:
            glTranslatef(-0.1, 0, 0)
        if key[pygame.K_UP]:
            glTranslatef(0, 0, 0.1)
        if key[pygame.K_DOWN]:
            glTranslate(0, 0, -0.1)
        if key[pygame.K_l]:
            mv += 0.05
            mv2 += 0.005

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Grid
        glPushMatrix()
        #glRotatef(angle, 0, 1, 0)
        draw_grid()
        glPopMatrix()

        # Pirámide
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslate(0, mv, 0)
        Pyramid()
        glPopMatrix()

        drawText(font, 20, 570, f'rotation speed: {speed_factor}',(0, 255, 0, 255),(0,0,0))
        angle += speed_factor
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
