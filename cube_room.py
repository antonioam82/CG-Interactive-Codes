import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def verts():
    global verticies
    verticies = [
    [1, -1, -1],#det inf der
    [1, 1, -1],#det sup der
    [-1, 1, -1],#det sup iz
    [-1, -1, -1],#det inf iz
    [1, -1, 1],#del inf der
    [1, 1, 1],#del sup der
    [-1, -1, 1],#del inf der
    [-1, 1, 1]#del sup iz
    ]

def major_verts():
    global verties
    verties = [
    [5, -2, -5],
    [5, 2, -5],#det sup der
    [-5, 2, -5],#det sup iz
    [-5, -2, -5],#det inf iz
    [5, -2, 5],#del inf der
    [5, 2, 5],#del sup der
    [-5, -2, 5],#del inf der
    [-5, 2, 5]#del sup iz
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
    (0,0,1),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,0),
    (1,0,0),
    (0,0,1),
    (1,0,1),
    (0,1,0),
    (1,0,0),
    (0,1,0),
    (0,1,0)
    )

def increase(o):
    global verticies
    if o == "inc":
        verticies[0][0]+=0.05
        verticies[0][1]-=0.05
        verticies[0][2]-=0.05
        verticies[1][0]+=0.05
        verticies[1][1]+=0.05
        verticies[1][2]-=0.05
        verticies[2][0]-=0.05
        verticies[2][1]+=0.05
        verticies[2][2]-=0.05
        verticies[3][0]-=0.05
        verticies[3][1]-=0.05
        verticies[3][2]-=0.05
        verticies[4][0]+=0.05
        verticies[4][1]-=0.05
        verticies[4][2]+=0.05
        verticies[5][0]+=0.05
        verticies[5][1]+=0.05
        verticies[5][2]+=0.05
        verticies[6][0]-=0.05
        verticies[6][1]-=0.05
        verticies[6][2]+=0.05
        verticies[7][0]-=0.05
        verticies[7][1]+=0.05
        verticies[7][2]+=0.05
    else:
        verticies[0][0]-=0.05
        verticies[0][1]+=0.05
        verticies[0][2]+=0.05
        verticies[1][0]-=0.05
        verticies[1][1]-=0.05
        verticies[1][2]+=0.05
        verticies[2][0]+=0.05
        verticies[2][1]-=0.05
        verticies[2][2]+=0.05
        verticies[3][0]+=0.05
        verticies[3][1]+=0.05
        verticies[3][2]+=0.05
        verticies[4][0]-=0.05
        verticies[4][1]+=0.05
        verticies[4][2]-=0.05
        verticies[5][0]-=0.05
        verticies[5][1]-=0.05
        verticies[5][2]-=0.05
        verticies[6][0]+=0.05
        verticies[6][1]+=0.05
        verticies[6][2]-=0.05
        verticies[7][0]+=0.05
        verticies[7][1]-=0.05
        verticies[7][2]-=0.05

def room():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verties[vertex])
    glEnd()
            

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x=0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()
        
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()
    
def main():
    global verticies, verties
    pygame.init()
    display = (700,500)#(1600,900)#(1200, 680)#(1600,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    major_verts()
    verts()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0,-5)
    #glRotatef(0, 0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        

        '''if keys[pygame.K_UP]:
            glRotatef(1, -1, 0, 0)
        if keys[pygame.K_DOWN]:
            glRotatef(1, 1, 0, 0)
        if keys[pygame.K_RIGHT]:
            glRotatef(1, 0, 9, 0)'''
        if keys[pygame.K_c]:
            verts()
        if keys[pygame.K_i]:
            increase("inc")
        if keys[pygame.K_o]:
            increase("dec")

        if keys[pygame.K_k]:
            verticies[1][1]-=0.019
            verticies[2][1]-=0.019
            verticies[5][1]-=0.019
            verticies[7][1]-=0.019
            verticies[3][1]+=0.019
            verticies[4][1]+=0.019
            verticies[6][1]+=0.019
            verticies[0][1]+=0.019

        if keys[pygame.K_l]:
            verticies[1][1]+=0.019
            verticies[2][1]+=0.019
            verticies[5][1]+=0.019
            verticies[7][1]+=0.019
            verticies[3][1]-=0.019
            verticies[4][1]-=0.019
            verticies[6][1]-=0.019
            verticies[0][1]-=0.019            
        
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 9, 0)
        room()
        Cube()
        
        pygame.display.flip()
        pygame.time.wait(10)

main()
