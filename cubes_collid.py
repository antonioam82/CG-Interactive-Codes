import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
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

def Cube(c):
    glLineWidth(2.0)
    glBegin(GL_LINES)
    if c == 'red':
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(0.0, 0.0, 1.0)# Color azul para el cubo
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST) 

    scale_factor = 1
    scale_factor2 = 1

    angle = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            scale_factor += 0.1
            scale_factor2 -= 0.1
            

        elif  key[pygame.K_DOWN]:
            scale_factor -= 0.1
            scale_factor2 += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Cubo 1
        glPushMatrix()
        #glTranslatef(-2, 0, 0)
        glTranslatef(0,0,0)
        glScalef(scale_factor, scale_factor, scale_factor)
        glRotatef(angle, 1, 1, 0)
        Cube('red')
        glPopMatrix()
        
        # Cubo 2
        glPushMatrix()
        #glTranslatef(2, 0, 0)
        glTranslatef(0,0,0)
        glScalef(scale_factor2, scale_factor2, scale_factor2)
        glRotatef(angle, -1, 1, 0)
        Cube('blue')
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
