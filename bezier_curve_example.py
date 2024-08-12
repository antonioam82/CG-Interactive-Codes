import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np  # Importar numpy para manejar los datos de manera eficiente

def initialize_window():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('OpenGL Evaluators Example')
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

def draw_bezier_curve():
    # Puntos de control de la curva de Bézier
    ctrlpoints = np.array([
        [-4.0, -4.0, 0.0],
        [-2.0, 4.0, 0.0],
        [2.0, -4.0, 0.0],
        [4.0, 4.0, 0.0]
    ], dtype='float32')  # Convertimos la lista en un array de numpy

    # Definir los puntos de control para el evaluador
    glMap1f(GL_MAP1_VERTEX_3, 0.0, 1.0, ctrlpoints)

    glEnable(GL_MAP1_VERTEX_3)

    # Dibujar la curva
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for i in range(101):
        glEvalCoord1f(i / 100.0)
    glEnd()

    # Dibujar los puntos de control
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for point in ctrlpoints:
        glVertex3fv(point)
    glEnd()

def main():
    initialize_window()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT)
        draw_bezier_curve()
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
