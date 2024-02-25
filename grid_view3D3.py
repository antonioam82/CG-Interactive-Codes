!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
    [1, 0, -1],
    [1, 1, -1],
    [-1, 1, -1],
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

'''# DIBUJA FIGURA
def Cube():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    glColor4f(0.0,0.0,0.1,0.5)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()
    
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()'''

# DIBUJA FIGURA CON EFECTO DE TRANSPARENCIA
def CubeT():

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    #glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    glColor4f(0.0,0.0,1.0,0.4)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()

    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    for edge in edges:
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()

# DEFINE FORMA DE LA FIGURA SOBRE EL GRID
def cube_form(val_list):
    val_list = val_list
    for i in range(0,8):
        verticies[i][1] = val_list[i]

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
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

cube_speed = 0.050 #0.00
camera_speed = 0.050
grid_size = 120
grid_spacing = 1
hide_data = False

# FUNCIÓN PRINCIPAL
def main():
    global cube_speed, camera_speed, hide_data, display_help
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 15)
    font2 = pygame.font.SysFont('arial', 20)
    direction = None

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
                        
                elif event.key == pygame.K_RIGHT:
                    print("definiendo derecha")
                    cube_form([0.0,0.5,1.0,0.0,0.0,0.5,0.0,1.0])
                    
                elif event.key == pygame.K_LEFT:
                    print("definiendo izquierda")
                    cube_form([0.0,1.0,0.5,0.0,0.0,1.0,0.0,0.5])
                    
                elif event.key == pygame.K_UP:
                    print("definiendo adelante")
                    cube_form([0.0,0.5,0.5,0.0,0.0,1.0,0.0,1.0])

                elif event.key == pygame.K_DOWN:
                    print("Definiendo atras")
                    cube_form([0.0,1.0,1.0,0.0,0.0,0.5,0.0,0.5])
                    
        key = pygame.key.get_pressed()

        # CONTROL DE DIRECCIÓN
        if key[pygame.K_LEFT]:
            direction = "Left"
            glTranslatef(camera_speed, 0.0, 0.0)
            verticies[0][0] -= cube_speed
            verticies[1][0] -= cube_speed
            verticies[2][0] -= cube_speed
            verticies[3][0] -= cube_speed
            verticies[4][0] -= cube_speed
            verticies[5][0] -= cube_speed
            verticies[6][0] -= cube_speed
            verticies[7][0] -= cube_speed
            
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
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        #Cube()
        CubeT()
        if not hide_data:
            drawText(font, 20, 570, f'cube speed: {cube_speed:.3f}',(0, 0, 255, 255),(0,0,0))#######################
            drawText(font, 20, 554, f'camera speed: {camera_speed:.3f}',(0, 0, 255, 255),(0,0,0))##########
            drawText(font, 20, 538, f'direction: {direction}',(0, 0, 255, 255),(0,0,0))
            
        direction = "None"
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
