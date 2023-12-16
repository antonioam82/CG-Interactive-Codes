import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

rotation_angle = 0  # Inicializar el ángulo de rotación
rotation_angle2 = 45

def draw_cube():
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glEnd()

def draw():
    global rotation_angle  # Acceder a la variable global de ángulo

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Dibujo de objeto 1
    glPushMatrix()
    glTranslatef(-1.5, 0.0, -6.0)  # Transformación para el objeto 1
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)  # Rotación para el objeto 1
    draw_cube()
    glPopMatrix()

    # Dibujo de objeto 2
    glPushMatrix()
    glTranslatef(1.5, 0.0, -6.0)  # Transformación para el objeto 2
    glRotatef(rotation_angle2, 0.0, 1.0, 0.0)  # Rotación para el objeto 2
    draw_cube()
    glPopMatrix()

    pygame.display.flip()

def main():
    global rotation_angle,rotation_angle2   # Acceder a la variable global de ángulo

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Rotar al presionar 'r'
                    rotation_angle += 10  # Aumentar el ángulo de rotación
                if event.key == pygame.K_t:  
                    rotation_angle2 -= 10 
        draw()
        clock.tick(60)

    pygame.quit()

main()
