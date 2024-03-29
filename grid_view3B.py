import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

'''vertices = (
    (-2, -2, 0),  # Esquina inferior izquierda (-2, -2, 0)
    (2, -2, 0),   # Esquina inferior derecha (2, -2, 0)
    (2, 2, 0),    # Esquina superior derecha (2, 2, 0)
    (-2, 2, 0)    # Esquina superior izquierda (-2, 2, 0)'''

verticies = [
    [1, 0, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, 0, -1],
    [1, 0, 1],
    [1, 1, 1],
    [-1, 0, 1],
    [-1, 1, 1]
    ]

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

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

# DIBUJA CONTORNOS DEL CUBO
def Cube():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0,)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()

# DIBUJA CUBO SOBRE EL GRID    
def CubeB():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    glColor3f(0.0,0.0,0.1)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

grid_size = 120
grid_spacing = 1

# DIBUJA GRID
def draw_grid():
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

# FUNCIÓN PRINCIPAL
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    x = 0.0
    z = 0.0
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(7, 1, 0, 0)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            x = 0.050
            z = 0.0
        if key[pygame.K_RIGHT]:
            x = -0.050
            z = 0.0
        if key[pygame.K_UP]:
            z = 0.050
            x = 0.0
        if key[pygame.K_DOWN]:
            z = -0.050
            x = 0.0
        if key[pygame.K_o]:
            x = 0.050
            z = 0.050
        if key[pygame.K_p]:
            x = -0.050
            z = 0.050
        if key[pygame.K_k]:
            x = -0.050
            z = -0.050
        if key[pygame.K_l]:
            x = 0.050
            z = -0.050 
        if key[pygame.K_s]:
            x = 0.0
            z = 0.0
            
        # ROTACIONES
        if key[pygame.K_q]:
            glRotatef(1, 0, 1, 0)
        if key[pygame.K_w]:
            glRotatef(1, 0, -1, 0)        
        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
        if key[pygame.K_g]:
            glRotatef(-0.1, 1, 0, 0)
        if key[pygame.K_e]:
            glRotatef(0.1, -1, 0, 0)
        if key[pygame.K_y]:
            glRotatef(0.1, 0, 0, 1)
        if key[pygame.K_u]:
            glRotatef(0.1, 0, 0, -1)

        glTranslatef(x, 0.0, z)  
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        CubeB()
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
