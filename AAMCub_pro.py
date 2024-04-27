import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120#10
grid_spacing = 1

vertices = [
    [1, 0.15, -1],#0
    [1, 2.15, -1],#1
    [-1, 2.15, -1],#2
    [-1, 0.15, -1],#3
    [1, 0.15, 1],#4
    [1, 2.15, 1],#5
    [-1, 0.15, 1],#6
    [-1, 2.15, 1]#7
    ]

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
    (5, 7))

def Cube():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glRotatef(1, 0, 1, 0)
    

def draw_grid():
    #glColor3f(0.0,1.0,0.0)#(0.5, 0.5, 0.5)  # Color gris
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.0, 0.0, 0.0, 1.0)#(0.0, 0.0, 1.0, 1.0)  # Establece el color de fondo en azul (RGB: 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    #glOrtho(-2, 2, -2, 2, -10, 25)
    glTranslatef(0.0, -1.5, -8.5)
    glRotatef(7, 1, 0, 0)
    angle = 0
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False

        key = pygame.key.get_pressed()

        if key[pygame.K_g]:
            glRotatef(-0.1, 1, 0, 0)

        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Grid
        glPushMatrix()
        #glRotatef(-angle, 0, 1, 0)
        draw_grid()
        glPopMatrix()

        # Cubo
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        Cube()
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()

