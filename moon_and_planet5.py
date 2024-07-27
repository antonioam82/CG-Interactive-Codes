import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

'''def draw_sphere():
    glColor3f(1.0, 0.0, 1.0)  # Color blanco
    gluSphere(gluNewQuadric(), 1, 32, 32)  # Crea una esfera con radio 1'''
        
def draw_sphere():
    glColor3f(0.0, 0.0, 0.0)
    #glColor3f(1.0, 1.0, 1.0)
    #glLineWidth(2)
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 1.002, 32, 32)  
    glColor3f(0.0, 0.0, 1.0) 
    gluSphere(gluNewQuadric(), 1, 32, 32)
    

# Rotacion para esfera menor
def draw_lit_sphere(rot): 
    glPushMatrix()#####3######3
    glLineWidth(1)
    #glColor3f(1.0, 1.0, 1.0)
    #gluSphere(gluNewQuadric(), 0.07, 10, 10)
    glColor3f(0.0, 1.0, 0.0)
    glScalef(2,2,1)
    glRotatef(-rot, 0, 0, 1)
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 0.07, 10, 10)  # Crea una esfera con radio 0.07
    glPopMatrix()

'''def draw_lit_sphere():
    glColor3f(0.0, 1.0, 0.0)  # Color verde
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)  # Establecer el estilo de dibujo a líneas
    gluSphere(quad, 0.07, 20, 20)  # Crea una esfera con radio 0.07'''
    
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
    #glRotatef(90, 1, 0, 0)
    #glRotatef(-23, 0, 1, 0)
    glRotatef(60, 1, 0, 0)

    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    scale_factor = 1.0
    distance = 1.3
    show_distance = True
    rot = 0
    angle = 1
    angle_lit = 1

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

        angle += 1
        angle_lit += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glScalef(scale_factor, scale_factor, scale_factor)

        glPushMatrix()
        glRotatef(angle, 0, 0, 1)  # Rotación para la esfera mayor
        draw_sphere()
        glPopMatrix()

        glPushMatrix()
        glRotatef(-angle_lit, 0, 0, 1)  # Traslacion en sentido contrario para la esfera menor
        glTranslatef(distance, 0.0, 0.0)
        draw_lit_sphere(rot)
        glPopMatrix()

        if show_distance:
            drawText(font, 20, 570, f'Distance: {distance:.3f}',(255, 255, 255, 255),(255,0,0))
        pygame.display.flip()
        clock.tick(30)
        rot += 10
            
    pygame.quit()

if __name__ == "__main__":
    main()
