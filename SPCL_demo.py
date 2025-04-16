#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#SPCL_demo.py en github

grid_size = 140
grid_spacing = 1


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
    glRotatef(15,1,0,0)
    glClearColor(0.3, 0.3, 0.3, 1.0)

    grid_list = draw_grid()

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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glCallList(grid_list)

        pygame.display.flip()
        pygame.time.wait(10)

    glDeleteLists(grid_list,1)
    pygame.quit()

if __name__=="__main__":
    main()
        
