import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

cube_speed = 0.050
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

# MOSTRAR TEXTO ESQUINA SUP. IZQUIERDA
def drawText(f, x, y, text):
    textSurface = f.render(text, True, (0, 0, 255, 255), (0, 0, 0))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

'''def make_rotation(c):
    if c == "N":'''
        

def main():
    global cube_speed
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)
    direction = None
    
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
            direction = "E"
            glTranslatef(0.050, 0.0, 0.0)
        if key[pygame.K_RIGHT]:
            direction = "W"
            glTranslatef(-0.050, 0.0, 0.0)
        if key[pygame.K_UP]:
            direction = "N"
            glTranslatef(0.0, 0.0, -0.050)
        if key[pygame.K_DOWN]:
            direction = "S"
            glTranslatef(0.0, 0.0, 0.050)

        if key[pygame.K_z]:
            cube_speed += 0.002
        if key[pygame.K_x]:
            cube_speed -= 0.002
        if key[pygame.K_c]:
            cube_speed = 0.050

        if key[pygame.K_q]:
            glRotatef(1, 0, 1, 0)
        if key[pygame.K_w]:
            glRotatef(1, 0, -1, 0)        
        if key[pygame.K_r]:
            glRotatef(0.1, 1, 0, 0)
        if key[pygame.K_g]:
            glRotatef(-0.1, 1, 0, 0)
        if key[pygame.K_y]:
            glRotatef(0.1, 0, 0, 1)
        if key[pygame.K_u]:
            glRotatef(0.1, 0, 0, -1)
        if key[pygame.K_o]:
            glRotatef(90, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        CubeB()
        # Guarda la matriz de transformación actual
        glPushMatrix()

        # Mueve el cubo a su posición deseada
        #glTranslatef(0.0, 0.0, -7.0)
        #glRotatef(7, 1, 0, 0)

        # Aplica rotación al cubo sin mover la cámara
        #glRotatef(1, 0, 1, 0)

        # Dibuja el cubo
        Cube()
        
        # Restaura la matriz de transformación original
        glPopMatrix()
        
        drawText(font, 20, 570, f'cube speed: {cube_speed:.3f}')
        drawText(font, 20, 554, 'camera speed: 0.050')
        drawText(font, 20, 538, f'direction: {direction}')
        
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()

main()
