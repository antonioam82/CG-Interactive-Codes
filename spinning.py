import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

rotate = False

def verts():
    global verticies
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
    

def Triangle():
    glBegin(GL_TRIANGLES)
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

def rotation():
    global rotate
    if rotate == True:
        rotate = False
    else:
        print("ndd")
        rotate = True
    
def main():
    global verticies
    pygame.init()
    display = (200,200)#(1598, 870)#(1200, 680)#(1600,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0, 0.1, 0.1, 1)
    

    verts()
    gluPerspective(35, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0,-5)
    #glRotatef(0, 0, 0, 0)

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
            glRotatef(5, 0, 1, 0)
        if keys[pygame.K_LEFT]:
            glRotatef(5, 0, -1, 0)
        if keys[pygame.K_k]:
            glRotatef(1, 0, 0, 1)
        if keys[pygame.K_l]:
            glRotatef(1, 0, 0, -1)
        if keys[pygame.K_p]:
            glRotatef(0, 0, 0, 0)
        if keys[pygame.K_c]:
            verts()
        if keys[pygame.K_z]:
            glTranslatef(0.0,0.0,-0.1)
        if keys[pygame.K_x]:
            glTranslatef(0.0,0.0,0.1)
        if keys[pygame.K_a]:
            glTranslatef(-0.1,0.0,0.0)
        if keys[pygame.K_s]:
            glTranslatef(0.1,0.0,0.0)
        if keys[pygame.K_q]:
            glTranslatef(0.0,-0.1,0.0)
        if keys[pygame.K_w]:
            glTranslatef(0.0,0.1,0.0)
        if keys[pygame.K_r]:
            #rotate = True
            rotation()
            time.sleep(1)

        if rotate:
            glRotatef(2, 0, 1, 0)
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    
        Triangle()
        
        pygame.display.flip()
        pygame.time.wait(10)

main()
