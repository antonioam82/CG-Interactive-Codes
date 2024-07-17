import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 120
grid_spacing = 1

def draw_grid():
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)  # Color verde

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

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

def draw_model(vertices, edges):
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    rot = 0

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(20,1,0,0)
    #glRotatef(25, 2, 1, 0)

    vertices, edges = load_obj('van.obj')  # Reemplaza 'your_model.obj' con la ruta de tu archivo .obj

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        glPushMatrix()
        glRotatef(-rot,0,1,0)
        draw_model(vertices, edges)
        glPopMatrix()
        rot += 0.6
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
