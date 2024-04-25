import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120#10
grid_spacing = 1

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

def draw_grid():
    #glColor3f(0.0,1.0,0.0)#(0.5, 0.5, 0.5)  # Color gris
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

def Cube(c):
    glLineWidth(2.0)
    glBegin(GL_LINES)
    if c == 'red':
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(0.0, 0.0, 1.0)# Color azul para el cubo
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST) 

    scale_factor = 1
    scale_factor2 = 1
    pos_x = 0
    pos_y = 0
    pos_z = 0

    angle = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            scale_factor += 0.1
            scale_factor2 -= 0.1
            

        elif  key[pygame.K_DOWN]:
            scale_factor -= 0.1
            scale_factor2 += 0.1

        elif key[pygame.K_w]:
            pos_z -= 0.1
        elif key[pygame.K_a]:
            pos_x -= 0.1
            

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Cubo 1
        glPushMatrix()
        #glTranslatef(-2, 0, 0)
        glTranslatef(pos_x,pos_y,pos_z)
        glScalef(scale_factor, scale_factor, scale_factor)
        glRotatef(angle, 1, 1, 0)
        Cube('red')
        glPopMatrix()
        
        # Cubo 2
        glPushMatrix()
        #glTranslatef(2, 0, 0)
        glTranslatef(0,-2,0)
        #glScalef(scale_factor2, scale_factor2, scale_factor2)
        #glRotatef(angle, 0, 1, 0)
        #Cube('blue')
        draw_grid()
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
