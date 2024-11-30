import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import math
import numpy as np

# Función para cargar el archivo OBJ
def load_obj(filename):
    vertices = []
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                parts = line.strip().split()
                # Las caras pueden tener más de 3 vértices, por lo tanto tenemos que manejar polígonos
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                for i in range(len(face_indices)):
                    edges.append((face_indices[i], face_indices[(i + 1) % len(face_indices)]))
    return vertices, edges

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

# Función para convertir un cuaternión a una matriz de rotación
class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def to_matrix(self):
        ww, xx, yy, zz = self.w * self.w, self.x * self.x, self.y * self.y, self.z * self.z
        wx, wy, wz = self.w * self.x, self.w * self.y, self.w * self.z
        xy, xz, yz = self.x * self.y, self.x * self.z, self.y * self.z

        return np.array([
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy), 0],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx), 0],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def __mul__(self, other):
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        )

# Función para crear un cuaternión de rotación a partir de un ángulo y un eje
def create_rotation_quaternion(angle, x, y, z):
    half_angle = math.radians(angle) / 2.0
    sin_half_angle = math.sin(half_angle)
    return Quaternion(math.cos(half_angle), x * sin_half_angle, y * sin_half_angle, z * sin_half_angle)

# Función para inicializar la proyección y la vista
def setup_view(display):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(50, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)

# Función principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)

    # Cargar el modelo OBJ
    #vertices, edges = load_obj('cube.obj')
    path = r'C:\Users\Usuario\Documents\repositorios\libigl-tutorial-data\truck.obj'
    model_name = os.path.basename(path)
    vertices, edges = load_obj(path)
    scale = 1
    hide_data = False

    # Crear la lista de display para el modelo
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glEndList()

    # Inicializar la vista y proyección
    setup_view(display)

    # Inicializar el cuaternión de rotación (sin rotación inicial)
    quaternion = Quaternion(1, 0, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_h:
                    if hide_data == True:
                        hide_data = False
                    else:
                        hide_data = True

        key = pygame.key.get_pressed()

        # Rotación con cuaterniones (si se presionan las teclas de dirección)
        if key[pygame.K_UP]:
            rotation = create_rotation_quaternion(2, 1, 0, 0)
            quaternion = quaternion * rotation
        if key[pygame.K_DOWN]:
            rotation = create_rotation_quaternion(-2, 1, 0, 0)
            quaternion = quaternion * rotation
        if key[pygame.K_RIGHT]:
            rotation = create_rotation_quaternion(2, 0, 1, 0)
            quaternion = quaternion * rotation
        if key[pygame.K_LEFT]:
            rotation = create_rotation_quaternion(-2, 0, 1, 0)
            quaternion = quaternion * rotation
        if key[pygame.K_m]:
            rotation = create_rotation_quaternion(-2, 0, 0, 1)
            quaternion = quaternion * rotation
        if key[pygame.K_n]:
            rotation = create_rotation_quaternion(2, 0, 0, 1)
            quaternion = quaternion * rotation
        if key[pygame.K_z]:
            scale += 0.05
        if key[pygame.K_x]:
            scale -= 0.05

        # Limpiar la pantalla y cargar la nueva matriz de rotación
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Convertir el cuaternión a matriz de rotación
        rotation_matrix = quaternion.to_matrix()
        glMultMatrixf(rotation_matrix)

        # Dibujar el modelo
        glScalef(scale,scale,scale)
        glCallList(model_list)

        glPopMatrix()

        if not hide_data:
            drawText(font, 20, 570, f'MODEL: {model_name}',(0, 255, 0, 255),(0,0,0))

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
