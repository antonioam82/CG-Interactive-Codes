#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120#10
grid_spacing = 1

vertices = (
    (1.0, 0.0, -1.0),
    (1.0, 0.5, -1.0),
    (-1.0, 0.5, -1.0),
    (-1.0, 0.0, -1.0),
    (1.0, 0.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 0.0, 1.0),
    (-1.0, 1.0, 1.0)
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

def Cube():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_QUADS)
    #glColor4f(0.0,0.0,1.0,0.4)
    glColor3f(0.0,0.0,1.0)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)
    font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)

    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    x = 0
    z = 0

    angle = 0
    stop = False
    running = True
    direction = 'front'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and direction != "back":
                    direction = "back"
                    angle = 180
                if event.key == pygame.K_UP and direction != "front":
                    direction = "front"
                    angle = 0
                if event.key == pygame.K_RIGHT and direction != "right":
                    direction = "right"
                    angle = -90
                if event.key == pygame.K_LEFT and direction != "left":
                    direction = "left"
                    angle = 90
                    
        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            z += 0.090
        elif key[pygame.K_DOWN]:
            z -= 0.090
        elif key[pygame.K_RIGHT]:
            x -= 0.090
        elif key[pygame.K_LEFT]:
            x += 0.090
            

        elif key[pygame.K_t]:
            glRotatef(1, 0, -0.1, 0)
        elif key[pygame.K_r]:
            glRotatef(1, 0, 0.1, 0)
        elif key[pygame.K_q]:
            glRotatef(1, -0.1, 0, 0)
        elif key[pygame.K_w]:
            glRotatef(1, 0.1, 0, 0)
        
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Grid
        glPushMatrix()
        glTranslatef(x, 0.0, z) 
        draw_grid()
        glPopMatrix()
        
        # Figura
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        Cube()
        glPopMatrix()

        drawText(font, 20, 570, f'f_direction: {direction}',(0, 255, 0, 255),(0,0,0))
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
