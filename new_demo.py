import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
    [1, -1, -1],  # Vertex 0
    [1, 1, -1],   # Vertex 1
    [-1, 1, -1],  # Vertex 2
    [-1, -1, -1], # Vertex 3
    [1, -1, 1],   # Vertex 4
    [1, 1, 1],    # Vertex 5
    [-1, -1, 1],  # Vertex 6
    [-1, 1, 1]    # Vertex 7
]


edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

# DIBUJA FIGURA
def Cube():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for edge in edges:  
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.0, 0.0, 0.0, 1.0)#(0.0, 0.0, 1.0, 1.0)  # Establece el color de fondo en azul (RGB: 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    #glTranslatef(0.0, -0.5, -10.0)
    glTranslatef(0.0, 0.0, -10.0)

    glScalef(1.0, 1.0, 9.0)
    
    #glRotatef(7, 1, 0, 0)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
                
        #glTranslatef(0.0, 0.0, 0.050)     
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
