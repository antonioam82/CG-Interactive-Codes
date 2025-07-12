#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

grid_size = 140
grid_spacing = 1

def load_obj(filename):
    vertices = []
    edges = []
    surfaces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                surfaces.append(face_indices)
                for i in range(len(face_indices)):
                    edges.append((face_indices[i], face_indices[(i + 1) % len(face_indices)]))
    
    return vertices, edges, surfaces

def draw_truck():
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glLineWidth(1.0)

    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    path = r'C:\Users\Usuario\Documents\fondo\truck.obj'
    vertices, edges, surfaces, = load_obj(path)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(0.2,0.5,0.3)
    glBegin(GL_TRIANGLES)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)
    glEndList()

    return model_list

def draw_back_fares():
    modelfb_list = glGenLists(1)
    glNewList(modelfb_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glLineWidth(1.0)

    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    path = r'C:\Users\Usuario\Documents\fondo\faros_traseros.obj'
    vertices, edges, surfaces, = load_obj(path)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(1.0,0.0,0.0)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)
    glEndList()

    return modelfb_list

def draw_fares():
    fmodel_list = glGenLists(1)
    glNewList(fmodel_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glLineWidth(1.0)

    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    path = r'C:\Users\Usuario\Documents\fondo\fares.obj'
    vertices, edges, surfaces, = load_obj(path)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(255, 140, 0)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)
    glEndList()

    return fmodel_list
        

def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    # Rellenar Grid
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glBegin(GL_QUADS)
    glColor3f(0.3,0.1,0.8)
    glVertex3f(-grid_size,0,-grid_size)
    glVertex3f(grid_size,0,-grid_size)
    glVertex3f(grid_size, 0, grid_size)
    glVertex3f(-grid_size, 0, grid_size)
    glEnd()
    #####################
    glLineWidth(1.3)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()
    glEndList()
    return grid_list

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 6)  # 4x multisample

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # ✅ Activar antialiasing después de crear el contexto OpenGL
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)

    font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)
    
    model_list = draw_truck()
    grid_list = draw_grid()
    fmodel_list = draw_fares()
    modelfb_list = draw_back_fares()
    hide_data = False

    x = z = x_c = z_c = angle = 0
    speed = 0.1
    speed_c = 0.1
    running = True
    direction = 'front'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and direction != "back":
                    direction = "back"; angle = 180
                elif event.key == pygame.K_UP and direction != "front":
                    direction = "front"; angle = 0
                elif event.key == pygame.K_RIGHT and direction != "right":
                    direction = "right"; angle = -90
                elif event.key == pygame.K_LEFT and direction != "left":
                    direction = "left"; angle = 90
                elif event.key == pygame.K_d:
                    speed = 0.1; speed_c = 0.1
                elif event.key == pygame.K_p:
                    speed_c = 0.0
                elif event.key == pygame.K_h:
                    hide_data = not hide_data
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_l:
                    direction = 'front'
                    x = z = x_c = z_c = angle = 0
                    speed = 0.1; speed_c = 0.1
                    glLoadIdentity()
                    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
                    glTranslatef(0.0, 0.0, -10)
                    glRotatef(15, 1, 0, 0)

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]: z += speed; z_c -= speed_c; z_c += speed
        if key[pygame.K_DOWN]: z -= speed; z_c += speed_c; z_c -= speed
        if key[pygame.K_RIGHT]: x -= speed; x_c += speed_c; x_c -= speed
        if key[pygame.K_LEFT]: x += speed; x_c -= speed_c; x_c += speed

        if key[pygame.K_t]: glRotatef(1, 0, -0.1, 0)
        elif key[pygame.K_r]: glRotatef(1, 0, 0.1, 0)
        elif key[pygame.K_q]: glRotatef(1, -0.1, 0, 0)
        elif key[pygame.K_w]: glRotatef(1, 0.1, 0, 0)

        if key[pygame.K_z]: speed += 0.001
        elif key[pygame.K_x]: speed -= 0.001
        elif key[pygame.K_c]: speed_c += 0.001
        elif key[pygame.K_v]: speed_c -= 0.001

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Grid
        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        glPopMatrix()

        # Truck
        glPushMatrix()
        glRotatef(-90,0,1,0)
        glCallList(model_list)
        glPopMatrix()

        # Truck_fares
        glPushMatrix()
        glRotatef(-90,0,1,0)
        glCallList(fmodel_list)
        glPopMatrix()

        # Truck back fares
        glPushMatrix()
        glRotatef(-90,0,1,0)
        glCallList(modelfb_list)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    glDeleteLists(grid_list, 1)
    pygame.quit()

main()

