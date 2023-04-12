import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


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

def Cubes():
    glBegin(GL_LINES)
    #glColor3d(0,1,3)
    #glBegin(GL_QUADS)
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

def cubes():
    glBegin(GL_LINES)
    #glColor3d(0,1,3)
    #glBegin(GL_QUADS)
    for e in lista_vertices:
        for edge in edges:
            for vertex in edge:
                glVertex3fv(e[vertex])

    glEnd()    
    

    
def main():
    global verticies, verticies1, verticies2, verticies3, verticies4, verticies5, verticies6
    pygame.init()
    display =(1598,870) #(800,600)#(1600,900)#(1200, 680)#(1200, 680)#(1600,900)
    func = 'A'
    clock = pygame.time.Clock()

    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0, 0, 1, 1)
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0,-20)#-5
    #glRotatef(0, 0, 0, 0)

    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.quit()
                #quit()
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_UP]:
            glRotatef(8, -1, 0, 0)
        if keys[pygame.K_DOWN]:
            glRotatef(8, 1, 0, 0)
        if keys[pygame.K_LEFT]:
            glRotatef(8, 0, 1, 0)
        if keys[pygame.K_RIGHT]:
            glRotatef(8, 0, -1, 0)
        if keys[pygame.K_k]:
            glRotatef(8, 0, 0, 1)
        if keys[pygame.K_l]:
            glTranslatef(-0.03, -0.03, -0.03)
        if keys[pygame.K_k]:
            glTranslatef(0.03, 0.03, 0.03)
        if keys[pygame.K_m]:
            verticies2[1][0] += 1
            verticies2[0][0] += 1
            verticies2[2][0] += 1
            verticies2[3][0] += 1
            verticies2[6][0] += 1
            verticies2[7][0] += 1
            verticies2[5][0] += 1
            verticies2[4][0] += 1
            
            verticies1[1][0] -= 1
            verticies1[0][0] -= 1
            verticies1[2][0] -= 1
            verticies1[3][0] -= 1
            verticies1[6][0] -= 1
            verticies1[7][0] -= 1
            verticies1[5][0] -= 1
            verticies1[4][0] -= 1

            verticies4[1][1] += 1
            verticies4[0][1] += 1
            verticies4[2][1] += 1
            verticies4[3][1] += 1
            verticies4[6][1] += 1
            verticies4[7][1] += 1
            verticies4[5][1] += 1
            verticies4[4][1] += 1

            verticies5[1][2] -= 1
            verticies5[0][2] -= 1
            verticies5[2][2] -= 1
            verticies5[3][2] -= 1
            verticies5[6][2] -= 1
            verticies5[7][2] -= 1
            verticies5[5][2] -= 1
            verticies5[4][2] -= 1
            
            verticies6[1][2] += 1
            verticies6[0][2] += 1
            verticies6[2][2] += 1
            verticies6[3][2] += 1
            verticies6[6][2] += 1
            verticies6[7][2] += 1
            verticies6[5][2] += 1
            verticies6[4][2] += 1
            
            verticies3[1][1] -= 1
            verticies3[0][1] -= 1
            verticies3[2][1] -= 1
            verticies3[3][1] -= 1
            verticies3[6][1] -= 1
            verticies3[7][1] -= 1
            verticies3[5][1] -= 1
            verticies3[4][1] -= 1

        if keys[pygame.K_n]:
            verticies2[1][0] -= 1
            verticies2[0][0] -= 1
            verticies2[2][0] -= 1
            verticies2[3][0] -= 1
            verticies2[6][0] -= 1
            verticies2[7][0] -= 1
            verticies2[5][0] -= 1
            verticies2[4][0] -= 1
    
            verticies1[1][0] += 1
            verticies1[0][0] += 1
            verticies1[2][0] += 1
            verticies1[3][0] += 1
            verticies1[6][0] += 1
            verticies1[7][0] += 1
            verticies1[5][0] += 1
            verticies1[4][0] += 1
            
            verticies4[1][1] -= 1
            verticies4[0][1] -= 1
            verticies4[2][1] -= 1
            verticies4[3][1] -= 1
            verticies4[6][1] -= 1
            verticies4[7][1] -= 1
            verticies4[5][1] -= 1
            verticies4[4][1] -= 1

            verticies5[1][2] += 1
            verticies5[0][2] += 1
            verticies5[2][2] += 1
            verticies5[3][2] += 1
            verticies5[6][2] += 1
            verticies5[7][2] += 1
            verticies5[5][2] += 1
            verticies5[4][2] += 1

            verticies6[1][2] -= 1
            verticies6[0][2] -= 1
            verticies6[2][2] -= 1
            verticies6[3][2] -= 1
            verticies6[6][2] -= 1
            verticies6[7][2] -= 1
            verticies6[5][2] -= 1
            verticies6[4][2] -= 1

            verticies3[1][1] += 1
            verticies3[0][1] += 1
            verticies3[2][1] += 1
            verticies3[3][1] += 1
            verticies3[6][1] += 1
            verticies3[7][1] += 1
            verticies3[5][1] += 1
            verticies3[4][1] += 1
        if keys[pygame.K_c]:
            if func == 'B':
                func = 'A'
            else:
                func = 'B'

        
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if func == 'A':
            Cubes()
        else:
            cubes()
        
        glRotatef(7, 2, 4, 3)
        pygame.display.flip()
        pygame.time.wait(30)
        #clock.tick(60)
        
    pygame.quit()
    #quit()

main()
