#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
    [1, 0, -1],
    [1, 0.5, -1],
    [-1, 0.5, -1],
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

# DIBUJA CUBO SOBRE EL GRID    
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

cube_speed = 0.050 #0.00
camera_speed = 0.050
grid_size = 120
grid_spacing = 1
hide_data = False
display_help = False

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
def drawText(f, x, y, text, c, bgc):
    #textSurface = f.render(text, True, (0, 0, 255, 255), (0, 0, 0))
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

# FUNCIÓN PRINCIPAL
def main():
    global cube_speed, camera_speed, hide_data, display_help
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)
    font2 = pygame.font.SysFont('arial', 20)
    direction = None
    #gluOrtho2D(0, 800, 0, 300)##

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(7, 1, 0, 0)
    
    running = True
    while (running):
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if hide_data == False:
                        hide_data = True
                    else:
                        hide_data = False
                        
                elif event.key == pygame.K_h:
                    if display_help == False:
                        display_help = True
                    else:
                        display_help = False
                        
                elif event.key == pygame.K_RIGHT:
                    print("definiendo derecha")
                    verticies[0][1] = 0.0
                    verticies[1][1] = 0.5
                    verticies[2][1] = 1.0
                    verticies[3][1] = 0.0
                    verticies[4][1] = 0.0
                    verticies[5][1] = 0.5
                    verticies[6][1] = 0.0
                    verticies[7][1] = 1.0
                    
                elif event.key == pygame.K_LEFT:
                    print("definiendo izquierda")
                    verticies[0][1] = 0.0
                    verticies[1][1] = 1.0
                    verticies[2][1] = 0.5
                    verticies[3][1] = 0.0
                    verticies[4][1] = 0.0
                    verticies[5][1] = 1.0
                    verticies[6][1] = 0.0
                    verticies[7][1] = 0.5
                    
                elif event.key == pygame.K_UP:
                    print("definiendo adelante")
                    verticies[0][1] = 0.0
                    verticies[1][1] = 0.5
                    verticies[2][1] = 0.5
                    verticies[3][1] = 0.0
                    verticies[4][1] = 0.0
                    verticies[5][1] = 1.0
                    verticies[6][1] = 0.0
                    verticies[7][1] = 1.0

                elif event.key == pygame.K_DOWN:
                    print("Definiendo atras")
                    verticies[0][1] = 0.0
                    verticies[1][1] = 1.0
                    verticies[2][1] = 1.0
                    verticies[3][1] = 0.0
                    verticies[4][1] = 0.0
                    verticies[5][1] = 0.5
                    verticies[6][1] = 0.0
                    verticies[7][1] = 0.5    
                    
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            direction = "Left"
            #glPushMatrix()
            glTranslatef(camera_speed, 0.0, 0.0)
            verticies[0][0] -= cube_speed
            verticies[1][0] -= cube_speed
            verticies[2][0] -= cube_speed
            verticies[3][0] -= cube_speed
            verticies[4][0] -= cube_speed
            verticies[5][0] -= cube_speed
            verticies[6][0] -= cube_speed
            verticies[7][0] -= cube_speed
            #glPopMatrix()
            
        if key[pygame.K_RIGHT]:
            direction = "Right"
            glTranslatef(-camera_speed, 0.0, 0.0)
            verticies[0][0] += cube_speed
            verticies[1][0] += cube_speed
            verticies[2][0] += cube_speed
            verticies[3][0] += cube_speed
            verticies[4][0] += cube_speed
            verticies[5][0] += cube_speed
            verticies[6][0] += cube_speed
            verticies[7][0] += cube_speed
            
        if key[pygame.K_UP]:
            direction = "Forward"
            glTranslatef(0.0, 0.0, camera_speed)
            verticies[0][2] -= cube_speed
            verticies[1][2] -= cube_speed
            verticies[2][2] -= cube_speed
            verticies[3][2] -= cube_speed
            verticies[4][2] -= cube_speed
            verticies[5][2] -= cube_speed
            verticies[6][2] -= cube_speed
            verticies[7][2] -= cube_speed
            
        if key[pygame.K_DOWN]:
            direction = "Backward"
            glTranslatef(0.0, 0.0, -camera_speed)
            verticies[0][2] += cube_speed
            verticies[1][2] += cube_speed
            verticies[2][2] += cube_speed
            verticies[3][2] += cube_speed
            verticies[4][2] += cube_speed
            verticies[5][2] += cube_speed
            verticies[6][2] += cube_speed
            verticies[7][2] += cube_speed        

        if key[pygame.K_z]:
            cube_speed += 0.002
        if key[pygame.K_x]:
            cube_speed -= 0.002
            
        if key[pygame.K_c]:
            cube_speed = camera_speed

        if key[pygame.K_b]:
            camera_speed += 0.002     
        if key[pygame.K_n]:
            camera_speed -= 0.002
                       
        # ROTACIONES
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

        if key[pygame.K_i]:
            '''verticies[0][2] -= 0.1
            verticies[1][2] -= 0.1
            verticies[2][2] -= 0.1
            verticies[3][2] -= 0.1
            verticies[4][2] -= 0.1
            verticies[5][2] -= 0.1
            verticies[6][2] -= 0.1
            verticies[7][2] -= 0.1'''
            glTranslatef(0.0, 0.0, 0.1)#################################

        if key[pygame.K_o]:
            glTranslatef(0.0, 0.0, -0.1)################################
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        CubeB()
        Cube()
        if not hide_data:
            drawText(font, 20, 570, f'cube speed: {cube_speed:.3f}',(0, 0, 255, 255),(0,0,0))#######################
            drawText(font, 20, 554, f'camera speed: {camera_speed:.3f}',(0, 0, 255, 255),(0,0,0))##########
            drawText(font, 20, 538, f'direction: {direction}',(0, 0, 255, 255),(0,0,0))
            
        if display_help:
            drawText(font2, 210, 500, '--------------------BUTTONS--------------------', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 480, 'Toggle help                                           H', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 460, 'Move foward                                    (UP)', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 440, 'Move backward                          (DOWN)', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 420, 'Move left                                      (LEFT)', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 400, 'Move right                                  (RIGHT)', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 380, 'Increase cube speed                             Z', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 360, 'Decrease cube speed                           X', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 340, 'Adjust cube speed to camera speed      C', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 320, 'Increase camera speed                         B', (255, 255, 255, 255),(0,0,255))
            drawText(font2, 210, 300, 'Decrease camera speed                        N', (255, 255, 255, 255),(0,0,255))
            
        direction = "None"
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
