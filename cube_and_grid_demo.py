#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120
grid_spacing = 1

'''verticies = [
    [1, 0, -1],
    [1, 0.5, -1],
    [-1, 0.5, -1],
    [-1, 0, -1],
    [1, 0, 1],
    [1, 0.5, 1],
    [-1, 0, 1],
    [-1, 0.5, 1]
    ]

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def Cube():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0,)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()'''

verticies = [
    [1, -1, -1],#inf, der, tras
    [1, 1, -1],#sup, der, tras
    [-1, 1, -1],#sup, izq, tras
    [-1, -1, -1],#inf, izq, tras
    [1, -1, 1],#inf, der, del
    [1, 1, 1],#sup, der, del
    [-1, -1, 1],#inf, izg, del
    [-1, 1, 1]#sup, izq, del
    ]

verticies1 = [
    [4, -1, -1],#inf, der, tras
    [4, 1, -1],#sup, der, tras
    [2, 1, -1],#sup, izq, tras
    [2, -1, -1],#inf, izq, tras
    [4, -1, 1],#inf, der, del
    [4, 1, 1],#sup, der, del
    [2, -1, 1],#inf, izg, del
    [2, 1, 1]#sup, izq, del
    ]

verticies2 = [
    [-4, -1, -1],#inf, der, tras
    [-4, 1, -1],#sup, der, tras
    [-2, 1, -1],#sup, izq, tras
    [-2, -1, -1],#inf, izq, tras
    [-4, -1, 1],#inf, der, del
    [-4, 1, 1],#sup, der, del
    [-2, -1, 1],#inf, izg, del
    [-2, 1, 1]#sup, izq, del        
    ]

verticies3 = [
    [1, 4, -1],#inf, der, tras
    [1, 2, -1],#sup, der, tras
    [-1, 2, -1],#sup, izq, tras
    [-1, 4, -1],#inf, izq, tras
    [1, 4, 1],#inf, der, del
    [1, 2, 1],#sup, der, del
    [-1, 4, 1],#inf, izg, del
    [-1, 2, 1]#sup, izq, del
    ]


verticies4 = [
    [1, -2, -1],#inf, der, tras
    [1, -4, -1],#sup, der, tras
    [-1, -4, -1],#sup, izq, tras
    [-1, -2, -1],#inf, izq, tras
    [1, -2, 1],#inf, der, del
    [1, -4, 1],#sup, der, del
    [-1, -2, 1],#inf, izg, del
    [-1, -4, 1]#sup, izq, del
    ]

verticies5 = [
    [1, -1, 4],#inf, der, tras
    [1, 1, 4],#sup, der, tras
    [-1, 1, 4],#sup, izq, tras
    [-1, -1, 4],#inf, izq, tras
    [1, -1, 2],#inf, der, del
    [1, 1, 2],#sup, der, del
    [-1, -1, 2],#inf, izg, del
    [-1, 1, 2]#sup, izq, del
    ]


verticies6 = [
    [1, -1, -2],#inf, der, tras
    [1, 1, -2],#sup, der, tras
    [-1, 1, -2],#sup, izq, tras
    [-1, -1, -2],#inf, izq, tras
    [1, -1, -4],#inf, der, del
    [1, 1, -4],#sup, der, del
    [-1, -1, -4],#inf, izg, del
    [-1, 1, -4]#sup, izq, del
    ]
    
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

colors = (
    (1,0,0),
    (1,0,0),
    (1,1,0),
    (1,0,1),
    (1,0,1),
    (1,0,0),
    (1,0,1),
    (1,0,1),
    (1,0,0),
    (1,1,0),
    (1,0,0),
    (1,1,0)
    )

colors2 = (
    (1,1,0),
    (1,0,1),
    (0,0.3,1),
    (0,0.7,0.4),
    (1,1,1),
    (0,0,0),
    (0.5,1,1),
    (1,1,0),
    (1,0,0),
    (0,0.5,1),
    (0,1,1),
    (1,0,0)
    )
        
lista_vertices = [verticies, verticies1, verticies2, verticies3, verticies4, verticies5, verticies6]

def cubes():
    glBegin(GL_LINES)

    glColor3f(1.0,1.0,0.0)
    for e in lista_vertices:
        for edge in edges:
            for vertex in edge:
                glVertex3fv(e[vertex])

    glEnd()
    glBegin(GL_QUADS)
    for i in lista_vertices:
        #glColor3d(0,1,0)
        for surface in surfaces:
            u=0
            for vertex in surface:
                u+=1
                glColor3fv(colors2[u])
                glVertex3fv(i[vertex])
    glEnd()


def draw_double_grid():
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)
    
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0.3, -grid_size)
        glVertex3f(x, 0.3, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0.3, z)
        glVertex3f(grid_size, 0.3, z)

    for a in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(a, -0.3, -grid_size)
        glVertex3f(a, -0.3, grid_size)

    for b in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, -0.3, b)
        glVertex3f(grid_size, -0.3, b)        

    glEnd()

# FUNCIÓN PRINCIPAL
def main():
    pygame.init()
    display =(900, 600)#(1600,870)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    x = 0.0
    z = 0.0
    r = 0.0
    
    glClearColor(0.5, 0.5, 0.5, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glRotatef(2, 1, 0, 0)
    glTranslatef(0,0,-20)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            x += 0.050
            z += 0.0
        if key[pygame.K_RIGHT]:
            x += -0.050
            z += 0.0
        if key[pygame.K_UP]:
            z += 0.050
            x += 0.0
        if key[pygame.K_DOWN]:
            z += -0.050
            x += 0.0
        if key[pygame.K_o]:
            x += 0.050
            z += 0.050
        if key[pygame.K_p]:
            x = -0.050
            z = 0.050
        if key[pygame.K_k]:
            x += -0.050
            z += -0.050
        if key[pygame.K_l]:
            x += 0.050
            z += -0.050 
        if key[pygame.K_s]:
            x += 0.0
            z += 0.0
            
        # ROTACIONES
        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
        if key[pygame.K_e]:
            glRotatef(-0.1, 1, 0, 0)
        if key[pygame.K_q]:
            glRotatef(0.5, 0, 1, 0)
        if key[pygame.K_w]:
            glRotatef(0.5, 0, -1, 0)        
        if key[pygame.K_g]:
            glRotatef(-0.5, 1, 0, 0)
        if key[pygame.K_y]:
            glRotatef(0.5, 0, 0, 1)
        if key[pygame.K_u]:
            glRotatef(0.5, 0, 0, -1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslatef(x, 0.0, z)  
        draw_double_grid()
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(r, 1, 1, 1)
        cubes()
        glPopMatrix()
        
        r += 0.9
        pygame.display.flip()
        pygame.time.wait(10)
        
    pygame.quit()
         
main()

