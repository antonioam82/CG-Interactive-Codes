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

grid_size = 120
grid_spacing = 1

# DIBUJA GRID
def draw_grid():
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor3f(0.0,1.0,0.0)#(0.5, 0.5, 0.5)  # Color gris
    
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    #glColor3f(1.0,0.0,0.0)
    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

def Cube():
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)  # Color azul para el cubo
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    scale_factor = 1.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scale_factor += 0.1
                if event.key == pygame.K_DOWN:
                    scale_factor -= 0.1'''

        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            scale_factor += 0.1

        elif  key[pygame.K_DOWN]:
            scale_factor -= 0.1
            
        
        glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -20.0)
        glRotatef(20, 1, 0, 0)
        draw_grid()
        glPopMatrix()
        glPushMatrix()
        glScalef(scale_factor, scale_factor, scale_factor)
        Cube()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
