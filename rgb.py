import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

verticies1 = [
    [1.5, -1.5, -1.5],#det inf der
    [1.5, 1.5, -1.5],#det sup der
    [-1.5, 1.5, -1.5],#det sup iz
    [-1.5, -1.5, -1.5],#det inf iz
    [1.5, -1.5, 1.5],#del inf der
    [1.5, 1.5, 1.5],#del sup der
    [-1.5, -1.5, 1.5],#del inf der
    [-1.5, 1.5, 1.5]#del sup iz
    ]    

verticies2 = [
    [2, -2, -2],#det inf der
    [2, 2, -2],#det sup der
    [-2, 2, -2],#det sup iz
    [-2, -2, -2],#det inf iz
    [2, -2, 2],#del inf der
    [2, 2, 2],#del sup der
    [-2, -2, 2],#del inf der
    [-2, 2, 2]#del sup iz
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
        

def increase(o):
    for i in lista_cubis:
        if o == "inc":
            i[0][0]+=0.05
            i[0][1]-=0.05
            i[0][2]-=0.05
            i[1][0]+=0.05
            i[1][1]+=0.05
            i[1][2]-=0.05
            i[2][0]-=0.05
            i[2][1]+=0.05
            i[2][2]-=0.05
            i[3][0]-=0.05
            i[3][1]-=0.05
            i[3][2]-=0.05
            i[4][0]+=0.05
            i[4][1]-=0.05
            i[4][2]+=0.05
            i[5][0]+=0.05
            i[5][1]+=0.05
            i[5][2]+=0.05
            i[6][0]-=0.05
            i[6][1]-=0.05
            i[6][2]+=0.05
            i[7][0]-=0.05
            i[7][1]+=0.05
            i[7][2]+=0.05
        else:
            i[0][0]-=0.05
            i[0][1]+=0.05
            i[0][2]+=0.05
            i[1][0]-=0.05
            i[1][1]-=0.05
            i[1][2]+=0.05
            i[2][0]+=0.05
            i[2][1]-=0.05
            i[2][2]+=0.05
            i[3][0]+=0.05
            i[3][1]+=0.05
            i[3][2]+=0.05
            i[4][0]-=0.05
            i[4][1]+=0.05
            i[4][2]-=0.05
            i[5][0]-=0.05
            i[5][1]-=0.05
            i[5][2]-=0.05
            i[6][0]+=0.05
            i[6][1]+=0.05
            i[6][2]-=0.05
            i[7][0]+=0.05
            i[7][1]-=0.05
            i[7][2]-=0.05
            
            
lista_cubis = [verticies,verticies1,verticies2]
colores_linea = [(1,0,0),(0,0,1),(0,1,0)]
print(colores_linea[0][0])
def Cube():
    glBegin(GL_LINES)
    #glColor3d(1, 0, 0)
    c=0
    for i in lista_cubis:
        glColor3d(colores_linea[c][0],colores_linea[c][1],colores_linea[c][2])
        for edge in edges:
            for vertex in edge:
                glVertex3fv(i[vertex])
        c+=1

    glEnd()
    
def main():
    #global verticies
    pygame.init()
    display = (500,500)#(1600,900)#(1200, 680)#(1600,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0,-5)
    #glRotatef(0, 0, 0, 0)
    glLineWidth(6)

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
        #if keys[pygame.K_LEFT]:
            #glRotatef(1, 0, -1, 0)
        if keys[pygame.K_k]:
            glRotatef(1, 0, 0, 1)
        if keys[pygame.K_l]:
            glRotatef(1, 0, 0, -1)
        if keys[pygame.K_c]:
            verts()
        if keys[pygame.K_z]:
            glTranslatef(0.0,0.0,-0.25)#-0.1)
        if keys[pygame.K_x]:
            glTranslatef(0.0,0.0,0.25)#0.1)
        if keys[pygame.K_i]:
            increase("inc")
        if keys[pygame.K_o]:
            increase("dec")
        if keys[pygame.K_a]:
            glTranslatef(-0.25,0.0,0.0)#(-0.1,0.0,0.0)

        if keys[pygame.K_s]:
            glTranslatef(0.25,0.0,0.0)#(0.1,0.0,0.0)
        if keys[pygame.K_q]:
            glTranslatef(0.0,-0.1,0.0)
        if keys[pygame.K_w]:
            glTranslatef(0.0,0.1,0.0)
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    
        Cube()
        glRotatef(1, 0, -1, 1)#0
        
        pygame.display.flip()
        pygame.time.wait(10)

main()
