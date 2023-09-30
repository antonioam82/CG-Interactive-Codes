import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

# DIBUJA CONTORNOS DEL CUBO
def Cube():
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()

# DIBUJA CUBO 
def CubeB():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    #glCullFace(GL_BACK)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.1)
    #glColor4f(0.0, 0.0, 0.1, 0.8)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

# FUNCIÓN PRINCIPAL
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    rot = False
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7.0)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        if key[pygame.K_p]:
            rot = True
        elif key[pygame.K_s]:
            rot = False
            
        # ROTACIONES
        if key[pygame.K_UP]:
            glRotatef(0.1, -1, 0, 0)       
        if key[pygame.K_DOWN]:
            glRotatef(0.1, 1, 0, 0)
            
        if rot == True:
            glRotatef(1, 0, 1, 0)
        glTranslatef(0.0, 0.0, 0.0)  
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        CubeB()
        Cube()

        #Cube()
        #CubeB()

        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
