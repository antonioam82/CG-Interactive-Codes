#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

os.chdir(r'C:\Users\Usuario\Documents\fondo')
# files_used

grid_size = 140
grid_spacing = 1

'''vertices = (
    (2.5, 0.0, -1.5),
    (2.0, 0.3, -1.0),
    (-2.0, 0.2, -1.0),
    (-2.5, 0.0, -1.5),
    (2.5, 0.2, 1.5),
    (2.0, 0.2, 1.0),
    (-2.5, 0.0, 1.5),
    (-2.0, 0.2, 1.0)
)'''

vertices = (
    (2.5, 0.0, -1.5),
    (2.0, 0.3, -1.0),
    (-2.0, 0.3, -1.0),
    (-2.5, 0.0, -1.5),
    (2.5, 0.0, 1.5),
    (2.0, 0.3, 1.0),
    (-2.5, 0.0, 1.5),
    (-2.0, 0.3, 1.0)
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
 
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def draw_plattform():
    platt_list = glGenLists(1)
    glNewList(platt_list, GL_COMPILE)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(0.2,0.4,0.3)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.0,0.0,0.0)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glEndList()
    return platt_list

def load_obj():
    vertices = []
    edges = set()
    faces = []
    filename = 'VideoShip.obj'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]),float(parts[3])]
                vertices.append(vertex)
            if line.startswith('f '):
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                faces.append(face_indices)
                for i in range(len(face_indices)):
                    edges.add(tuple(sorted((face_indices[i], face_indices[(i + 1) % len(face_indices)]))))
    return vertices, edges, faces


'''def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
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
    return grid_list'''

'''def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 1.0)  # Azul

    for x in range(-grid_size, grid_size, grid_spacing):
        for z in range(-grid_size, grid_size, grid_spacing):
            glVertex3f(x, 0, z)
            glVertex3f(x + grid_spacing, 0, z)
            glVertex3f(x + grid_spacing, 0, z + grid_spacing)
            glVertex3f(x, 0, z + grid_spacing)

    glEnd()
    glEndList()
    return grid_list'''

'''def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)

    # 1. cuadro
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 1.0)  # Azul
    for x in range(-grid_size, grid_size, grid_spacing):
        for z in range(-grid_size, grid_size, grid_spacing):
            glVertex3f(x, 0, z)
            glVertex3f(x + grid_spacing, 0, z)
            glVertex3f(x + grid_spacing, 0, z + grid_spacing)
            glVertex3f(x, 0, z + grid_spacing)
    glEnd()

    # lineas
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0.002, -grid_size)  # +0.001 para evitar z-fighting
        glVertex3f(x, 0.002, grid_size)
    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0.002, z)
        glVertex3f(grid_size, 0.002, z)
    glEnd()

    glEndList()
    return grid_list'''

def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)

    # 1. Dibujar un solo cuadrado azul para el fondo
    glEnable(GL_POLYGON_OFFSET_FILL)#############
    glPolygonOffset(1.0, 1.0)####################
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)  # Azul
    glVertex3f(-grid_size, 0, -grid_size)
    glVertex3f(grid_size, 0, -grid_size)
    glVertex3f(grid_size, 0, grid_size)
    glVertex3f(-grid_size, 0, grid_size)
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)###########

    # 2. Dibujar las líneas blancas por encima
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)  # Blanco
    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0.002, -grid_size)
        glVertex3f(x, 0.002, grid_size)
    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0.002, z)
        glVertex3f(grid_size, 0.002, z)
    glEnd()

    glEndList()
    return grid_list


def initial_view():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 90.0)
    glTranslatef(0.0, 0.0, -10)
    glRotatef(15, 1, 0, 0)
    
def main():
    pygame.init()
    display = (800, 600)
    #pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    #gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
    #glTranslatef(0.0,0.0,-10)
    
    

    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 6)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    #glRotatef(15,1,0,0)
    glClearColor(0.3, 0.3, 0.3, 1.0)

    initial_view() #######################################################

    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # antialiasing
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    top = False
    view_elevation = -10.0
    vele = 0.0 ###############
    elevation = 2.6
    z_pos = 0.0
    fly_speed = 0.0

    model_vertices, edges, faces = load_obj()
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(model_vertices[vertex])
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0,0.0,1.0)
    for face in faces:
        for vertex in face:
            glVertex3fv(model_vertices[vertex])
    glEnd()
    glEndList()

    grid_list = draw_grid()
    platt_list = draw_plattform()
    

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_i: # Top View
                    initial_view() #################################################
                    glRotatef(75,1,0,0)
                    glRotatef(-90,0,1,0)
                    glTranslatef(0.0,-10.0,0.0)
                    top = True #######################
                    vele = 0.0 #######################
                elif event.key == pygame.K_l:
                    fly_speed = 2.0
                elif event.key == pygame.K_m:
                    fly_speed = 0.0
                    elevation = 2.6
                    z_pos = 0.0
                           
        key_button = pygame.key.get_pressed()

        # Rotaciones
        if key_button[pygame.K_r]:
            glRotatef(0.8,0,1,0)
        elif key_button[pygame.K_t]:
            glRotatef(-0.8,0,1,0)
        elif key_button[pygame.K_y]:
            glRotatef(0.8,1,0,0)
        elif key_button[pygame.K_u]:
            glRotatef(-0.8,1,0,0)
        elif key_button[pygame.K_o]:
            glRotatef(-0.8,0,0,1)
        elif key_button[pygame.K_p]:
            glRotatef(0.8,0,0,1)
            
        # Tralaciones
        if key_button[pygame.K_c]:
            glTranslatef(0.0,0.0,-0.05)
        if key_button[pygame.K_v]:
            glTranslatef(0.0,0.0,0.05)
        if key_button[pygame.K_d]:
            glTranslatef(-0.05,0.0,0.0)
        if key_button[pygame.K_f]:
            glTranslatef(0.05,0.0,0.0)
        if key_button[pygame.K_b]:
            glTranslatef(0.0,0.05,0.0)
        if key_button[pygame.K_n]:
            glTranslatef(0.0,-0.05,0.0)
            
        # Spaceship elevation
        if key_button[pygame.K_j]:
            elevation += 0.04
        if key_button[pygame.K_k] and elevation > 2.6:
            elevation -= 0.04
        

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        vele += 0.2#################################################
        
        if vele < 27.00 and top: ###################################
            glTranslatef(0.0,0.08,0.0)##############################
            print(vele)#############################################

        glCallList(grid_list)
        glCallList(platt_list)
        
        glPushMatrix()
        glScalef(0.2,0.2,0.2)
        glColor3f(1.0,0.0,0.0)
        glTranslatef(1.0,elevation,0.0)
        glRotatef(-90,0,1,0)
        glLineWidth(1.0)
        glPushMatrix()
        glTranslatef(0.0,0.0,z_pos)
        glCallList(model_list)
        glPopMatrix()
        glPopMatrix()

        z_pos += fly_speed

        pygame.display.flip()
        pygame.time.wait(10)

    glDeleteLists(grid_list,1)
    glDeleteLists(platt_list,1)
    glDeleteLists(model_list,1)
    
    pygame.quit()

if __name__=="__main__":
    main()

        
