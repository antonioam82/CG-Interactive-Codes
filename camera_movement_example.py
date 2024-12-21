import pygame
import numpy as np

# Clase FreeCamera simulando un movimiento en 3D
class FreeCamera:
    def __init__(self, position=np.array([0, 0, -5], dtype=float), speed=2.0):
        self.position = np.array(position, dtype=float)  # Posición 3D de la cámara
        self.speed = speed  # Velocidad de movimiento

    def update(self, dt, keys):
        if keys[pygame.K_UP]:  # Adelante (eje Z, hacia adelante)
            self.move_forward(dt)
        if keys[pygame.K_DOWN]:  # Atrás (eje Z, hacia atrás)
            self.move_backward(dt)
        if keys[pygame.K_LEFT]:  # Izquierda (eje X)
            self.strafe_left(dt)
        if keys[pygame.K_RIGHT]:  # Derecha (eje X)
            self.strafe_right(dt)

    def move_forward(self, dt):
        self.position[2] += self.speed * dt  # Movimiento hacia adelante (eje Z positivo)

    def move_backward(self, dt):
        self.position[2] -= self.speed * dt  # Movimiento hacia atrás (eje Z negativo)

    def strafe_left(self, dt):
        self.position[0] -= self.speed * dt  # Movimiento en el eje X (izquierda)

    def strafe_right(self, dt):
        self.position[0] += self.speed * dt  # Movimiento en el eje X (derecha)

    def get_position(self):
        return self.position

# Función para proyectar puntos 3D en la pantalla 2D
def project_point(point, camera_position, screen_size):
    fov = 500  # Campo de visión (field of view)
    x, y, z = point - camera_position

    if z > 0:  # Evitar dividir por cero y objetos detrás de la cámara
        factor = fov / z  # Factor de proyección para simular perspectiva
        x_2d = int(x * factor + screen_size[0] / 2)
        y_2d = int(-y * factor + screen_size[1] / 2)
        return (x_2d, y_2d)
    return None

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana de Pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Free Camera Example in 3D")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Variables para el bucle principal
clock = pygame.time.Clock()
running = True

# Crear la cámara
camera = FreeCamera(position=[0, 0, -10], speed=10.0)

# Crear un objeto cúbico en 3D (un cubo centrado en el origen)
cube_vertices = np.array([
    [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1],  # Frente
    [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1]   # Atrás
], dtype=float)

# Tamaño del cubo
cube_size = 2
cube_vertices *= cube_size

# Bucle principal
while running:
    dt = clock.tick(60) / 1000  # Delta time en segundos (para 60 FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()

    # Actualizar la cámara según la entrada del usuario
    camera.update(dt, keys)

    # Dibujar el fondo blanco
    screen.fill(WHITE)

    # Proyectar los puntos del cubo 3D en la pantalla 2D
    projected_points = []
    for vertex in cube_vertices:
        projected = project_point(vertex, camera.get_position(), screen.get_size())
        if projected:
            projected_points.append(projected)

    # Dibujar las aristas del cubo
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Frente
        (4, 5), (5, 6), (6, 7), (7, 4),  # Atrás
        (0, 4), (1, 5), (2, 6), (3, 7)   # Conexiones entre frente y atrás
    ]
    for edge in edges:
        start, end = edge
        if start < len(projected_points) and end < len(projected_points):
            pygame.draw.line(screen, BLUE, projected_points[start], projected_points[end], 2)

    # Mostrar la posición de la cámara en pantalla
    font = pygame.font.SysFont(None, 36)
    position_text = font.render(f'Posición de la cámara: {camera.get_position()}', True, BLACK)
    screen.blit(position_text, (20, 20))

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()

