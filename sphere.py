import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

'''def draw_sphere():
    glColor3f(1.0, 0.0, 1.0)  # Color blanco
    gluSphere(gluNewQuadric(), 1, 32, 32)  # Crea una esfera con radio 1'''

def draw_sphere():
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 1, 32, 32)  # Crea una esfera con radio 1'''

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -3)  # Mueve la esfera hacia atrás para que sea visible
    glRotatef(90, 1, 0, 0)
    glRotatef(-23, 0, 1, 0)
    
    scale_factor = 1.0 ######################
    

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #___________________________________
        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            scale_factor += 0.1

        elif  key[pygame.K_DOWN]:
            scale_factor -= 0.1
        #____________________________________
        
        #glRotatef(1, 3, 1, 1)  # Rotación de la esfera
        glRotatef(1, 0, 0, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()#####3######3
        glScalef(scale_factor, scale_factor, scale_factor)
        draw_sphere()
        glPopMatrix()###################3
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
