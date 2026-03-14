import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- Configuración y Datos ---
grid_size = 140
vertices = [(1,0,-1), (1,0.5,-1), (-1,0.5,-1), (-1,0,-1), (1,0,1), (1,1,1), (-1,0,1), (-1,1,1)]
edges = [(0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)]
surfaces = [(0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6)]

def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5) # Gris para no cansar la vista
    for i in range(-grid_size, grid_size + 1):
        glVertex3f(i, 0, -grid_size); glVertex3f(i, 0, grid_size)
        glVertex3f(-grid_size, 0, i); glVertex3f(grid_size, 0, i)
    glEnd()
    glEndList()
    return grid_list

def draw_cube():
    cube_list = glGenLists(1)
    glNewList(cube_list, GL_COMPILE)
    # Caras
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.4, 0.8)
    for surface in surfaces:
        for vertex in surface: glVertex3fv(vertices[vertex])
    glEnd()
    # Bordes
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for edge in edges:
        for vertex in edge: glVertex3fv(vertices[vertex])
    glEnd()
    glEndList()
    return cube_list

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Python Runner")
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0, -2.0, -15.0) # Ajuste inicial de cámara
    glRotatef(20, 1, 0, 0)

    grid_id = draw_grid()
    cube_id = draw_cube()

    # Variables de estado
    pos_x, pos_z = 0, 0
    angle = 0
    cam_speed = 0.1
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False
                # Rotación según dirección
                if event.key == K_UP:    angle = 0
                if event.key == K_DOWN:  angle = 180
                if event.key == K_LEFT:  angle = 90
                if event.key == K_RIGHT: angle = -90

        # Movimiento fluido
        keys = pygame.key.get_pressed()
        if keys[K_UP]:    pos_z += cam_speed
        if keys[K_DOWN]:  pos_z -= cam_speed
        if keys[K_LEFT]:  pos_x += cam_speed
        if keys[K_RIGHT]: pos_x -= cam_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar Suelo (se mueve con la "cámara")
        glPushMatrix()
        glTranslatef(pos_x, 0, pos_z)
        glCallList(grid_id)
        glPopMatrix()

        # Dibujar Cubo (estático en el centro de la pantalla, o puedes moverlo)
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glCallList(cube_id)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60) # 60 FPS estables

    pygame.quit()

if __name__ == "__main__":
    main()
