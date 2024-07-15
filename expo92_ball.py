import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sphere():
    glColor3f(1.0, 0.0, 0.0)  # Color blanco
    gluSphere(gluNewQuadric(), 1, 32, 32)  # Crea una esfera con radio 1
    glColor3f(1.0, 1.0, 0.0)
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 1, 32, 32)
    #gluSphere(quad, 1.003, 32, 32)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Mueve la esfera hacia atrás para que sea visible

    '''glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)'''
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glRotatef(1, 3, 3, 2)  # Rotación de la esfera

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_sphere()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
