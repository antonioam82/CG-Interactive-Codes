#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

grid_size = 170
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

    min_v = np.min(vertices, axis=0)
    max_v = np.max(vertices, axis=0)
    center = (min_v + max_v) / 2.0
    vertices = [list(np.array(v) - center) for v in vertices]
    
    return vertices, edges, surfaces

def draw_walls():
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)#################################
    glEnable(GL_POLYGON_OFFSET_FILL)##################################
    glPolygonOffset(1.0, 1.0)
    glLineWidth(1.6)  # Set line width (optional)
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,0.0)
    path = r'C:\Users\anton\Downloads\maze_large_with_plazesss.obj'
    vertices, edges, surfaces = load_obj(path)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glColor3f(0.2,0.5,0.3)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)################################
    glEndList()
    return model_list

def draw_grid():
    grid_list = glGenLists(1)
    glNewList(grid_list, GL_COMPILE)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0,1.0)
    glBegin(GL_QUADS)
    
    glColor3f(0.3,0.2,0.4)
    glVertex3f(-grid_size,0,-grid_size)
    glVertex3f(grid_size,0,-grid_size)
    glVertex3f(grid_size, 0, grid_size)
    glVertex3f(-grid_size, 0, grid_size)
    
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)########### 
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
    
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
    
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
    glTranslatef(0.0, 0.0, -10)
    
    glEnable(GL_DEPTH_TEST)
    #font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)

    #cube_list = Cube()
    grid_list = draw_grid()
    #other_list = other_cube()
    model_list = draw_walls()
    #hide_data = False

    #############################################3
    rotating = False
    rotation_speed = 2.0
    target_angle = 0
    current_angle = 0
    index = 0
    ###############################################

    scale = 1.0
    x = 0
    z = 0

    speed = 0.1

    directions = ['front','right','back','left']

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:   # Detectar teclas presionadas
                if event.key == pygame.K_ESCAPE: # Si es ESC, salir
                    running = False

                elif event.key == pygame.K_RIGHT and not rotating:
                    index += 1
                    if index > 3:
                        index = 0
                    direction = directions[index]
                    target_angle += 90
                    rotating = True
                    print(direction)
                elif event.key == pygame.K_LEFT and not rotating:
                    index -= 1
                    if index < 0:
                        index = 3
                    direction = directions[index]
                    target_angle -= 90
                    rotating = True
                    print(direction)        

        key = pygame.key.get_pressed()

        #TRANSLACIONES
        if key[pygame.K_UP] and not rotating:
            if direction == 'front':
                z += speed
            elif direction == 'back':
                z -= speed
            elif direction == 'right':
                x -= speed
            elif direction == 'left':
                x += speed
            
        elif key[pygame.K_DOWN] and not rotating:
            if direction == 'front':
                z -= speed
            elif direction == 'back':
                z += speed
            elif direction == 'right':
                x += speed
            elif direction == 'left':
                x -= speed
        '''elif key[pygame.K_LEFT] and not rotating:
            glTranslatef(0.2,.0,0.0)
        elif key[pygame.K_RIGHT] and not rotating:
            glTranslatef(-0.2,.0,0.0)

        elif key[pygame.K_m]:
             glRotatef(1,1,0,0)
        elif key[pygame.K_n]:
             glRotatef(-1,1,0,0)'''

        if rotating:
            angle_difference = target_angle - current_angle
            if abs(angle_difference) > rotation_speed:
                if angle_difference > 0:
                    current_angle += rotation_speed
                    glRotatef(rotation_speed, 0, 1, 0)
                else:
                    current_angle -= rotation_speed
                    glRotatef(-rotation_speed, 0, 1, 0)
            else:
                glRotatef(angle_difference, 0, 1, 0)
                current_angle = target_angle
                rotating = False
            
        '''elif key[pygame.K_z]:
            scale += 1.0
        elif key[pygame.K_x]:
            scale -= 1.0'''
                  

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glScalef(scale,scale,scale)

        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        
        glPushMatrix()
        
        glScalef(0.3,0.09,0.3)######################
        glRotatef(90, 1, 0, 0)
        glTranslatef(0.0, 0.0, -26.2)
        glTranslatef(0.0, 1.9, 0.0)
        glScalef(35.0,35.0,35.0)
        glCallList(model_list)
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

        glFlush()
        pygame.display.flip()
        pygame.time.wait(10)

main()
pygame.quit()


