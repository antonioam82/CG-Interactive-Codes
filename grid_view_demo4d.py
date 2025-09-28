#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

grid_size = 140
grid_spacing = 1

another_cube = (
    (1.0, 0.0, -1.0),
    (1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, 0.0, -1.0),
    (1.0, 0.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 0.0, 1.0),
    (-1.0, 1.0, 1.0)
)

vertices = (
    (1.0, 0.0, -1.0),
    (1.0, 0.5, -1.0),
    (-1.0, 0.5, -1.0),
    (-1.0, 0.0, -1.0),
    (1.0, 0.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 0.0, 1.0),
    (-1.0, 1.0, 1.0)
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

def draw_walls():
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)#################################
    glEnable(GL_POLYGON_OFFSET_FILL)##################################
    glPolygonOffset(1.0, 1.0)
    glLineWidth(1.6)  # Set line width (optional)
    
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,0.0)
    path = r'C:\Users\anton\OneDrive\Documentos\files_used\temple_maze.obj' 
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

def show_controls():
    print("\n--------------------- Controls ---------------------")
    
    print("\nKeyboard Controls:")
    print("  - Up Arrow: Move forward in the scene")
    print("  - Down Arrow: Move backward in the scene")
    print("  - Left Arrow: Move left in the scene")
    print("  - Right Arrow: Move right in the scene")
    
    print("\nRotation Controls:")
    print("  - 'T' Key: Rotate the scene clockwise")
    print("  - 'R' Key: Rotate the scene counterclockwise")
    print("  - 'Q' Key: Tilt the scene upwards")
    print("  - 'W' Key: Tilt the scene downwards")
    
    print("\nSpeed Controls:")
    print("  - 'Z' Key: Increase camera movement speed")
    print("  - 'X' Key: Decrease camera movement speed")
    print("  - 'C' Key: Increase figure movement speed")
    print("  - 'V' Key: Decrease figure movement speed")
    
    print("\nMiscellaneous:")
    print("  - 'H' Key: Toggle visibility of on-screen data")
    print("  - 'P' Key: Pause the figure movement")
    
    print("\n----------------------------------------------------")


def Cube():
    cube_list = glGenLists(1)
    glNewList(cube_list, GL_COMPILE)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.0,0.0,1.0)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glEndList()
    return cube_list

def other_cube():
    #other_cube_list = glGenLists(1)
    #glNewList(other_cube_list, GL_COMPILE)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    #glColor3f(0.2, 0.4, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(another_cube[vertex])
    glEnd()

    glBegin(GL_QUADS)
    r = random.uniform(0.0,1.0)
    g = random.uniform(0.0,1.0)
    b = random.uniform(0.0,1.0)
    glColor3f(r,g,b)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(another_cube[vertex])
    glEnd()

    #glEndList()
    #return other_cube_list

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

# Variables globales para controlar la rotación
rotation_speed = 2.0  # velocidad de rotación por frame (más baja es más lenta)
target_angle = 0
current_angle = 0
rotating = False

def main():
    pygame.init()
    display = (1600, 900)
    
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
    
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(0.0, 0.0, -10)
    
    glEnable(GL_DEPTH_TEST)
    font = pygame.font.SysFont('arial', 15)
    #glRotatef(15, 1, 0, 0)
    glRotatef(55, 1, 0, 0)

    cube_list = Cube()
    grid_list = draw_grid()
    #other_list = other_cube()
    model_list = draw_walls()
    hide_data = True

    show_controls()

    x = 0
    z = 0

    x_c = 0
    z_c = 0

    global current_angle, target_angle, rotating
    speed = 0.1
    speed_c = 0.1
    running = True
    direction = 'front'
    scale = 0.55#1.0
    
    rot = 0
    cube_translation = -20.0
    sentido = "LEFT"
    fall_speed = 0.0
    y_ = 0.001
    
    scene = 0
    index = 0
    directions = ['front', 'right', 'back', 'left']

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                # Rotación a la derecha
                if event.key == pygame.K_RIGHT and not rotating:
                    index += 1
                    if index > 3:
                        index = 0
                    direction = directions[index]
                    target_angle += 90
                    rotating = True
                
                # Rotación a la izquierda
                elif event.key == pygame.K_LEFT and not rotating:
                    index -= 1
                    if index < 0:
                        index = 3
                    direction = directions[index]
                    target_angle -= 90
                    rotating = True

                elif event.key == pygame.K_d:
                    speed = 0.1
                    speed_c = 0.1
                elif event.key == pygame.K_p:
                    speed_c = 0.000
                elif event.key == pygame.K_h:
                    hide_data = not hide_data
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_l:
                    direction = 'front'
                    current_angle = 0
                    target_angle = 0
                    angle_diference = 0
                    index = 0
                    x = 0
                    z = 0
                    x_c = 0
                    z_c = 0
                    angle = 0
                    speed = 0.1
                    speed_c = 0.1
                    scale = 1.0
        
                    # Restaurar las rotaciones acumuladas
                    glLoadIdentity()  # Resetea las transformaciones
                    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)  # Reestablece la perspectiva
                    glTranslatef(0.0, 0.0, -10)  # Reestablece la cámara alejada
                    glRotatef(15, 1, 0, 0)

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            if direction == 'front':# and z + speed <= (grid_size - 1):
                if z + speed > (grid_size + 0.5):
                    fall_speed = spd#0.05
                    
                z += speed
                z_c -= speed_c
                z_c += speed
                
            elif direction == 'back':# and z - speed >= (-grid_size + 1):
                '''if z - speed >= (-grid_size + 1):
                    fall_speed = 0.05'''
                    
                z -= speed
                z_c += speed_c
                z_c -= speed
            elif direction == 'right':# and x - speed >= (-grid_size + 1):
                '''if x - speed >= (-grid_size + 1):
                    fall_speed = 0.05'''
                    
                x -= speed
                x_c += speed_c
                x_c -= speed##########################'''
            elif direction == 'left' and x + speed <= (grid_size - 1):
                '''if x + speed <= (grid_size - 1):
                    fall_speed = 0.05'''
                    
                x += speed
                x_c -= speed_c
                x_c += speed
            
        if key[pygame.K_DOWN]:
            if direction == 'front':
                z -= speed
                z_c += speed_c
                z_c -= speed
            elif direction == 'back':
                z += speed
                z_c -= speed_c
                z_c += speed
            elif direction == 'right':
                x += speed
                x_c -= speed_c
                x_c += speed
            elif direction == 'left':
                x -= speed
                x_c += speed_c
                x_c -= speed

        # Rotations and scalations
        if key[pygame.K_y]:
            glRotatef(1, 0, -0.1, 0)
        elif key[pygame.K_r]:
            glRotatef(1, 0, 0.1, 0)
        elif key[pygame.K_q]:
            if direction == 'front':
                glRotatef(1, -0.1, 0, 0)
            elif direction == 'back':
                glRotatef(1, 0.1, 0, 0)
            elif direction == 'right':
                glRotatef(1, 0, 0, -0.1)
            elif direction == 'left':
                glRotatef(1, 0, 0, 0.1)
            '''if direction == 'front' or direction == 'back':
                glRotatef(1, -0.1, 0, 0)
            else:  #elif direction == 'right' or direction == 'left':
                glRotatef(1, 0, 0, -0.1)
        elif key[pygame.K_k]:
            glTranslatef(0.0,-0.1,0.0)
        elif key[pygame.K_j]:
            glTranslatef(0.0,0.1,0.0)'''
            
        elif key[pygame.K_w]:
            if direction == 'front':
                glRotatef(1, 0.1, 0, 0)
            elif direction == 'back':
                glRotatef(1, -0.1, 0, 0)
            elif direction == 'right':
                glRotatef(1, 0, 0, 0.1)
            elif direction == 'left':
                glRotatef(1, 0, 0, -0.1)
            '''if direction == 'front' or direction == 'back':
                glRotatef(1, 0.1, 0, 0)
            else:
                glRotatef(1, 0, 0, 0.1)'''
        elif key[pygame.K_a]:
            scale += 0.01
        elif key[pygame.K_s]:
            scale -= 0.01
            

        # Change speed
        elif key[pygame.K_z]:
            speed += 0.001
            speed_c += 0.001
        elif key[pygame.K_x]:
            speed -= 0.001
            speed_c -= 0.001
            
        ########################################################33
        elif key[pygame.K_k]:
            #camera_dist += 0.5
            glTranslatef(0.0, 0.0, -0.02)
        elif key[pygame.K_j]:
            glTranslatef(0.0, 0.0, 0.02)
        ##########################################################
            

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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glScalef(scale,scale,scale)

        # Dibujar el grid
        glPushMatrix()
        #glRotatef(1, 90, 0, 0)
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -17.5)
        glTranslatef(0.0, 1.9, 0.0)
        glScalef(10.0,10.0,10.0)
        glCallList(model_list)
        glPopMatrix()
        glPushMatrix()################################3
        glTranslatef(cube_translation, 0.0, -80.5)
        glRotatef(rot, 0.0, 1.0, 0.0)
        #glCallList(other_list)
        other_cube()
        glPopMatrix()####################################
        glPopMatrix()

        # Dibujar el cubo
        glPushMatrix()
        glTranslatef(x_c, 0.0, z_c)
        glTranslatef(0.0,y_,0.0)
        glRotatef(-current_angle, 0, 1, 0)
        glCallList(cube_list)
        glPopMatrix()
        glPopMatrix()

        rot += 3

        if cube_translation >= -37.0 and sentido == "LEFT":
            cube_translation -= 0.25
            #print("TO LEFT: ",cube_translation)
        else:
            sentido = "RIGHT"

        if cube_translation <= -19.2 and sentido == "RIGHT":
            cube_translation += 0.25
            #print("TO RIGHT: ",cube_translation)
        else:
            sentido = "LEFT"

        spd = round(speed, 3)
        spdc = round(speed_c, 3)

        if not hide_data:
            drawText(font, 20, 570, f'DIRECTION: {direction}', (0, 255, 0, 255), (0, 0, 0))
            drawText(font, 20, 550, f'CAMERA SPEED: {spd}', (0, 255, 0, 255), (0, 0, 0))
            drawText(font, 20, 530, f'FIGURE SPEED: {spdc}', (0, 255, 0, 255), (0, 0, 0))
            drawText(font, 20, 510, f'SCALE: {scale:.2f}', (0, 255, 0, 255), (0, 0, 0))

        y_ -= fall_speed

        glFlush()
        pygame.display.flip()
        pygame.time.wait(10)

main()
pygame.quit()

