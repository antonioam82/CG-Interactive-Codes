import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

#os.chdir(r'C:\Users\Usuario\Desktop\DATOS RECUPERADOS Antonio\Documents\pruebas')
os.chdir(r'C:\Users\Usuario\Desktop\DATOS RECUPERADOS Antonio\Documents\Nueva carpeta')

# Vértices del cubo
vertices = [
    [1, 0.15, -1], # 0
    [1, 2.15, -1], # 1
    [-1, 2.15, -1], # 2
    [-1, 0.15, -1], # 3
    [1, 0.15, 1],  # 4
    [1, 2.15, 1],  # 5
    [-1, 0.15, 1], # 6
    [-1, 2.15, 1]  # 7
]

# Caras del cubo
faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

# Coordenadas de textura: Se aplican a cada cara individualmente
# Estas coordenadas cubrirán completamente la textura en cada cara
texture_coords = [
    [(0, 0), (1, 0), (1, 1), (0, 1)],  # Cara frontal
    [(0, 0), (1, 0), (1, 1), (0, 1)],  # Cara trasera
    [(0, 0), (1, 0), (1, 1), (0, 1)],  # Cara derecha
    [(0, 0), (1, 0), (1, 1), (0, 1)],  # Cara izquierda
    [(0, 0), (1, 0), (1, 1), (0, 1)],  # Cara superior
    [(0, 0), (1, 0), (1, 1), (0, 1)]   # Cara inferior
]

# Función para cargar la textura
def load_texture():
    texture_surface = pygame.image.load('dob.jpg')  # Asegúrate de que la ruta sea correcta
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)  # Habilitar texturas
    texture_id = glGenTextures(1)  # Generar ID de textura
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texture_id

# Función para dibujar el cubo con texturas aplicadas
def Cube(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincular la textura

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        for j, vertex in enumerate(face):
            glTexCoord2fv(texture_coords[i][j])  # Coordenada de textura para cada vértice
            glVertex3fv(vertices[vertex])  # Dibuja cada vértice de la cara
    glEnd()

# Dibuja el grid (opcional, para referencia)
def draw_grid():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    grid_size = 120
    grid_spacing = 1
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -8.0)
    glEnable(GL_DEPTH_TEST)

    texture_id = load_texture()  # Cargar la textura

    angle = 0
    scale_x = 1
    scale_y = 1
    scale_z = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()

        if key[pygame.K_a]:
            scale_x += 0.01
            scale_z += 0.01
        if key[pygame.K_s]:
            scale_x -= 0.01
            scale_z -= 0.01

        if key[pygame.K_q]:
            scale_y += 0.01
        if key[pygame.K_w]:
            scale_y -= 0.01

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibuja el grid
        glPushMatrix()
        draw_grid()
        glPopMatrix()

        # Dibuja el cubo con la textura
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glScalef(scale_x, scale_y, scale_z)
        Cube(texture_id)
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

main()
