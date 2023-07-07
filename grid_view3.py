import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120
grid_spacing = 1

def draw_grid():
    glBegin(GL_LINES)
    glColor3f(0.0,1.0,0.0)#(0.5, 0.5, 0.5)  # Color gris

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
    x = 0.0
    z = 0.0
    persp = 0.1

    glClearColor(0.0, 0.0, 0.0, 1.0)#(0.0, 0.0, 1.0, 1.0)  # Establece el color de fondo en azul (RGB: 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) #45
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(7, 1, 0, 0)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            x = 0.050
            z = 0.0
        if key[pygame.K_RIGHT]:
            x = -0.050
            z = 0.0
        if key[pygame.K_UP]:
            z = 0.050
            x = 0.0
        if key[pygame.K_DOWN]:
            z = -0.050
            x = 0.0
        if key[pygame.K_o]:
            x = 0.050
            z = 0.050
        if key[pygame.K_p]:
            x = -0.050
            z = 0.050
        if key[pygame.K_k]:
            x = -0.050
            z = -0.050
        if key[pygame.K_l]:
            x = 0.050
            z = -0.050
        if key[pygame.K_s]:
            x = 0.0
            z = 0.0

        glTranslatef(x, 0.0, z)
        #glRotatef(1, 1, 2, 1)
        #glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
