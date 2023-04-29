import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def verts():
    global verticies
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

def C1_verts():
    global verticies1#hor, vert, prof
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

def C2_verts():
    global verticies2
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

def C3_verts():
    global verticies3
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

def C4_verts():
    global verticies4
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

def C5_verts():
    global verticies5
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

def C6_verts():
    global verticies6
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
        

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()

def Cube1():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies1[vertex])
    glEnd()

def Cube2():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies2[vertex])
    glEnd()
    
def Cube3():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies3[vertex])
    glEnd()

def Cube4():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies4[vertex])
    glEnd()

def Cube5():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies5[vertex])
    glEnd()

def Cube6():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies6[vertex])
    glEnd()

def persp(n,display):###############################################################################3
    gluPerspective(90+n, (display[0]/display[1]), 0.1, 50.0)

    
def main():
    global verticies, verticies1, verticies2, verticies3, verticies4, verticies5, verticies6
    pygame.init()
    display = (500,500)#(1598, 870)#(1598, 870)#(1200, 680)#(1600,900)#1598,870
    
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.5, 0.5, 0.9, 1)

    verts()
    C1_verts()
    C2_verts()
    C3_verts()
    C4_verts()
    C5_verts()
    C6_verts()
    
    gluPerspective(85, (display[0]/display[1]), 0.1, 50.0)#90  #120
    #persp(0,display)############################################################################################
    glTranslatef(0.0,0.0,-4)#-5 #-4
    #glRotatef(0, 0, 0, 0)
    glLineWidth(2)
    glColor3d(1,0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_UP]:
            glRotatef(1, -1, 0, 0)
        if keys[pygame.K_DOWN]:
            glRotatef(1, 1, 0, 0)
        if keys[pygame.K_RIGHT]:
            glRotatef(1, 0, 1, 0)
        if keys[pygame.K_LEFT]:
            glRotatef(10, 0, -1, 0)
        if keys[pygame.K_k]:
            glRotatef(1, 0, 0, 1)
        if keys[pygame.K_l]:
            glRotatef(1, 0, 0, -1)
        #if keys[pygame.K_z]:
            #persp(0.0000000001,display)#################################################################################
            #glTranslatef(0.0,0.0,-0.1)
        #if keys[pygame.K_x]:
            #glTranslatef(0.0,0.0,0.1)
        if keys[pygame.K_m]:
            verticies2[1][0] += 0.07 #0.07
            verticies2[0][0] += 0.07
            verticies2[2][0] += 0.07
            verticies2[3][0] += 0.07
            verticies2[6][0] += 0.07
            verticies2[7][0] += 0.07
            verticies2[5][0] += 0.07
            verticies2[4][0] += 0.07
            
            verticies1[1][0] -= 0.07
            verticies1[0][0] -= 0.07
            verticies1[2][0] -= 0.07
            verticies1[3][0] -= 0.07
            verticies1[6][0] -= 0.07
            verticies1[7][0] -= 0.07
            verticies1[5][0] -= 0.07
            verticies1[4][0] -= 0.07

            verticies4[1][1] += 0.07
            verticies4[0][1] += 0.07
            verticies4[2][1] += 0.07
            verticies4[3][1] += 0.07
            verticies4[6][1] += 0.07
            verticies4[7][1] += 0.07
            verticies4[5][1] += 0.07
            verticies4[4][1] += 0.07

            verticies5[1][2] -= 0.07
            verticies5[0][2] -= 0.07
            verticies5[2][2] -= 0.07
            verticies5[3][2] -= 0.07
            verticies5[6][2] -= 0.07
            verticies5[7][2] -= 0.07
            verticies5[5][2] -= 0.07
            verticies5[4][2] -= 0.07
            
            verticies6[1][2] += 0.07
            verticies6[0][2] += 0.07
            verticies6[2][2] += 0.07
            verticies6[3][2] += 0.07
            verticies6[6][2] += 0.07
            verticies6[7][2] += 0.07
            verticies6[5][2] += 0.07
            verticies6[4][2] += 0.07
            
            verticies3[1][1] -= 0.07
            verticies3[0][1] -= 0.07
            verticies3[2][1] -= 0.07
            verticies3[3][1] -= 0.07
            verticies3[6][1] -= 0.07
            verticies3[7][1] -= 0.07
            verticies3[5][1] -= 0.07
            verticies3[4][1] -= 0.07

        if keys[pygame.K_n]:
            verticies2[1][0] -= 0.07
            verticies2[0][0] -= 0.07
            verticies2[2][0] -= 0.07
            verticies2[3][0] -= 0.07
            verticies2[6][0] -= 0.07
            verticies2[7][0] -= 0.07
            verticies2[5][0] -= 0.07
            verticies2[4][0] -= 0.07
    
            verticies1[1][0] += 0.07
            verticies1[0][0] += 0.07
            verticies1[2][0] += 0.07
            verticies1[3][0] += 0.07
            verticies1[6][0] += 0.07
            verticies1[7][0] += 0.07
            verticies1[5][0] += 0.07
            verticies1[4][0] += 0.07
            
            verticies4[1][1] -= 0.07
            verticies4[0][1] -= 0.07
            verticies4[2][1] -= 0.07
            verticies4[3][1] -= 0.07
            verticies4[6][1] -= 0.07
            verticies4[7][1] -= 0.07
            verticies4[5][1] -= 0.07
            verticies4[4][1] -= 0.07

            verticies5[1][2] += 0.07
            verticies5[0][2] += 0.07
            verticies5[2][2] += 0.07
            verticies5[3][2] += 0.07
            verticies5[6][2] += 0.07
            verticies5[7][2] += 0.07
            verticies5[5][2] += 0.07
            verticies5[4][2] += 0.07

            verticies6[1][2] -= 0.07
            verticies6[0][2] -= 0.07
            verticies6[2][2] -= 0.07
            verticies6[3][2] -= 0.07
            verticies6[6][2] -= 0.07
            verticies6[7][2] -= 0.07
            verticies6[5][2] -= 0.07
            verticies6[4][2] -= 0.07

            verticies3[1][1] += 0.07
            verticies3[0][1] += 0.07
            verticies3[2][1] += 0.07
            verticies3[3][1] += 0.07
            verticies3[6][1] += 0.07
            verticies3[7][1] += 0.07
            verticies3[5][1] += 0.07
            verticies3[4][1] += 0.07
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    
        Cube()
        Cube1()
        Cube2()
        Cube3()
        Cube4()
        Cube5()
        Cube6()
        
        glRotatef(1, 0, 1, 0)
        pygame.display.flip()
        pygame.time.wait(10)

main()
