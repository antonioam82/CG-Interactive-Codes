import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Vertices del cubo
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

# Edges del cubo
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

# Dibuja el cubo
def draw_cube():
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Dibuja el plano (cuadrado)
def draw_plane():
    glColor3f(1.0,1.0,1.0)
    glBegin(GL_QUADS)
    glVertex3f(-5, -1, -5)
    glVertex3f(-5, -1, 5)
    glVertex3f(5, -1, 5)
    glVertex3f(5, -1, -5)
    glEnd()

# Función principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    # Posición inicial del cubo
    cube_x, cube_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Captura de teclas para mover el cubo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cube_x -= 1.2
        if keys[pygame.K_RIGHT]:
            cube_x += 1.2
        if keys[pygame.K_UP]:
            cube_y += 1.2
        if keys[pygame.K_DOWN]:
            cube_y -= 1.2

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibuja el plano
        draw_plane()

        glPushMatrix()
        # Traslada el cubo a su nueva posición
        #glTranslatef(cube_x, cube_y, 0.0)
        glRotatef(cube_x,cube_y,cube_x,cube_y)
        # Dibuja el cubo
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
