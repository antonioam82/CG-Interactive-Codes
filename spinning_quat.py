#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np


verticies = [
    [0, 1, 0],#top
    [1, 0, -1],#del der
    [-1, 0, -1],#del iz
    [1, 0, 1],#tras der
    [-1, 0, 1],#tras iz
    [0, -1, 0]#bottom
    ]
    
edges =(
    (0,1),
    (0,2),
    (0,3),
    (0,4),
    (1,3),
    (2,1),
    (4,2),
    (4,3),
    (5,1),
    (5,2),
    (5,3),
    (5,4)
    )

surfaces = (
    (3,0,4),
    (4,0,2),
    (2,0,1),
    (1,0,3),
    (3,5,4),
    (4,5,2),
    (2,5,1),
    (1,5,3)
    )


colors = (
    (1,1,0),
    (0,1,0),
    (1,0,1),
    (0,1,1),
    (0,1,1),
    (0,1,0),
    )

def draw_figure():
    glBegin(GL_TRIANGLES)
    for surface in surfaces:
        x=0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    #glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(35, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0,-5)
    glRotatef(90,1,0,0)

    #line_color = 0.0
    rot = 1.2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(rot,0,1,0)
        draw_figure()
        
        pygame.display.flip()
        pygame.time.wait(10)

        '''if line_color < 1.0:
            line_color += 0.001'''

    pygame.quit()

if __name__ =="__main__":
    main()
