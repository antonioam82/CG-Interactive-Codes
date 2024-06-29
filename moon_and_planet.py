import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
        
def draw_sphere():
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 1, 32, 32)  # Crea una esfera con radio 1'''

def draw_lit_sphere():
    glColor3f(0.0, 1.0, 0.0)  # Color blanco
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 0.07, 20, 20)  # Crea una esfera con radio 1'''

def drawText(f, x, y, text, c, bgc):
    #textSurface = f.render(text, True, (0, 0, 255, 255), (0, 0, 0))
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -3)  # Mueve la esfera hacia atrás para que sea visible
    glRotatef(90, 1, 0, 0)
    glRotatef(-23, 0, 1, 0)

    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    scale_factor = 1.0
    distance = 1.3
    show_distance = True
    

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if show_distance:
                        show_distance = False
                    else:
                        show_distance = True
                elif event.key == pygame.K_UP:
                    scale_factor += 0.01
                elif event.key == pygame.K_DOWN:
                    scale_factor -= 0.01
        #___________________________________
        key = pygame.key.get_pressed()
        
        if  key[pygame.K_o]:
            distance += 0.02
        elif  key[pygame.K_p]:
            distance -= 0.02 
        #____________________________________

        glRotatef(1, 0, 0, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glScalef(scale_factor, scale_factor, scale_factor)
        draw_sphere()
        glPushMatrix()#####3######3
        glTranslatef(distance, 0.0, 0.0)
        draw_lit_sphere()
        glPopMatrix()###################3

        if show_distance:
            drawText(font, 20, 570, f'Distance: {distance:.3f}',(255, 255, 255, 255),(255,0,0))
        pygame.display.flip()
        clock.tick(30)
            
    pygame.quit()

if __name__ == "__main__":
    main()

