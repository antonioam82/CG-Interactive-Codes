import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

'''vertices = (
    (-2, -2, 0),  # Esquina inferior izquierda (-2, -2, 0)
    (2, -2, 0),   # Esquina inferior derecha (2, -2, 0)
    (2, 2, 0),    # Esquina superior derecha (2, 2, 0)
    (-2, 2, 0)    # Esquina superior izquierda (-2, 2, 0)'''

verticies = [
    [1, 0, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, 0, -1],
    [1, 0, 1],
    [1, 1, 1],
    [-1, 0, 1],
    [-1, 1, 1]
    ]

'''verticies2 = [
    [1, 0, -2],
    [1, 1, -2],
    [-1, 1, -2],
    [-1, 0, -2],
    [1, 0, 0],
    [1, 1, 0],
    [-1, 0, 0],
    [-1, 1, 0]
    ]'''

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
    
'''def Cube2():
    #glBegin(GL_QUADS)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    #for surface in surfaces:
    for edge in edges:  
        x=0
        #for vertex in surface:
        for vertex in edge:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(verticies2[vertex])
    glEnd()'''

def Cube(v1,v2):
    glLineWidth(1.5)#
    glBegin(GL_LINES)
    '''r = round(random.uniform(0.4,1),2)
    g = round(random.uniform(0.4,1),2)
    b = round(random.uniform(0.4,1),2)'''
    r = random.randint(0,1)
    g = random.randint(0,1)
    b = random.randint(0,1)
    glColor3f(r,g,b)
    verticies[0][2] = v1
    verticies[1][2] = v1
    verticies[2][2] = v1
    verticies[3][2] = v1
    verticies[4][2] = v2
    verticies[5][2] = v2
    verticies[6][2] = v2
    verticies[7][2] = v2
    for edge in edges:
        x = 0
        for vertex in edge:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

grid_size = 120
grid_spacing = 1

'''def draw_grid():
    glBegin(GL_LINES)
    glColor3f(0.0,1.0,0.0)#(0.5, 0.5, 0.5)  # Color gris

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    #glColor3f(1.0,0.0,0.0)
    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()'''

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(7, 1, 0, 0)
    speed = 0.050 # VELOCIAD HACIA ADELANTE
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            glTranslatef(0.050, 0.0, 0.0)
        if key[pygame.K_RIGHT]:
            glTranslatef(-0.050, 0.0, 0.0)
        if key[pygame.K_UP]:
            glTranslatef(0.0, 0.0, speed)
            speed += 0.0008 # AUMENTO VELOCIDAD
        if key[pygame.K_DOWN]:
            glTranslatef(0.0, 0.0, -0.050)
        if key[pygame.K_o]:
            glTranslatef(0.050, 0.0, 0.050)
        if key[pygame.K_p]:
            glTranslatef(-0.050, 0.0, 0.050)
        if key[pygame.K_k]:
            glTranslatef(-0.050, 0.0, -0.050)
        if key[pygame.K_l]:
            glTranslatef(0.050, 0.0, -0.050)

        # ROTACIONES
        if key[pygame.K_q]:
            glRotatef(0.1, 0, 1, 0)
        if key[pygame.K_w]:
            glRotatef(0.1, 0, -1, 0)        
        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
        if key[pygame.K_g]:
            glRotatef(-0.1, 1, 0, 0)
        if key[pygame.K_e]:
            glRotatef(0.1, -1, 0, 0)
        if key[pygame.K_y]:
            glRotatef(0.1, 0, 0, 1)
        if key[pygame.K_u]:
            glRotatef(0.1, 0, 0, -1)
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #draw_grid()
        v1 = -1
        v2 = 0
        for i in range(50):
            Cube(v1,v2)
            v1 -= 1
            v2 -= 1
            
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
