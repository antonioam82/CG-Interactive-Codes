#/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

grid_size = 140
grid_spacing = 1

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

def draw_grid():
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
    print("  - 'D' Key: Reset speeds to default")
    print("  - 'L' Key: Restore the view to the original position")
    print("  - 'ESC' Key: Close the application (close window)")

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

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

TARGET_FPS = 120.0

def main():
    pygame.init()
    display = (800, 600)

    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 6)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_MULTISAMPLE)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)
    font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)
    scale = 1.0

    cube_list = Cube()
    grid_list = draw_grid()
    hide_data = False

    show_controls()
    rot_x = 15.0
    rot_y = 0.0
    ROT_SPEED = 60.0   

    x = 0
    z = 0
    x_c = 0
    z_c = 0

    angle = 0
    speed   = 12.0   
    speed_c = 12.0

    SPEED_STEP = 0.12

    running = True
    direction = 'front'

    clock = pygame.time.Clock()
    last_time = time.perf_counter()

    while running:
        now = time.perf_counter()
        dt = abs(min(now - last_time, 0.05))
        last_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and direction != "back":
                    direction = "back"
                    angle = 180
                elif event.key == pygame.K_UP and direction != "front":
                    direction = "front"
                    angle = 0
                elif event.key == pygame.K_RIGHT and direction != "right":
                    direction = "right"
                    angle = -90
                elif event.key == pygame.K_LEFT and direction != "left":
                    direction = "left"
                    angle = 90
                elif event.key == pygame.K_d:
                    speed   = 12.0
                    speed_c = 12.0
                elif event.key == pygame.K_p:
                    speed_c = 0.0
                elif event.key == pygame.K_h:
                    hide_data = not hide_data
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_l:
                    direction = 'front'
                    x = 0;  z = 0
                    x_c = 0; z_c = 0
                    angle = 0
                    scale = 1.0
                    speed   = 12.0
                    speed_c = 12.0
                    rot_x = 15.0
                    rot_y = 0.0

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            z   +=  speed * dt
            z_c -= (speed - speed_c) * dt
        if key[pygame.K_DOWN]:
            z   -=  speed * dt
            z_c += (speed - speed_c) * dt
        if key[pygame.K_RIGHT]:
            x   -=  speed * dt
            x_c += (speed - speed_c) * dt   
        if key[pygame.K_LEFT]:
            x   +=  speed * dt
            x_c -= (speed - speed_c) * dt

        if key[pygame.K_a]:
            scale += 0.3 * TARGET_FPS * dt
        elif key[pygame.K_s]:
            scale -= 0.3 * TARGET_FPS * dt

        if key[pygame.K_t]:
            rot_y -= ROT_SPEED * dt
        elif key[pygame.K_r]:
            rot_y += ROT_SPEED * dt

        if key[pygame.K_q]:
            rot_x -= ROT_SPEED * dt
        elif key[pygame.K_w]:
            rot_x += ROT_SPEED * dt

        if key[pygame.K_z]:
            speed   += SPEED_STEP * TARGET_FPS * dt
        elif key[pygame.K_x]:
            speed   -= SPEED_STEP * TARGET_FPS * dt
        if key[pygame.K_c]:
            speed_c += SPEED_STEP * TARGET_FPS * dt
        elif key[pygame.K_v]:
            speed_c -= SPEED_STEP * TARGET_FPS * dt

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
        glTranslatef(0.0, 0.0, -10)

        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        glScalef(scale, scale, scale)

        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(x_c, 0.0, z_c)
        glRotatef(angle, 0, 1, 0)
        glCallList(cube_list)
        glPopMatrix()

        if not hide_data:
            drawText(font, 20, 570, f'DIRECTION: {direction}',   (0, 255, 0, 255), (0,0,0))
            drawText(font, 20, 550, f'CAMERA SPEED: {speed_c:.3f}',(0, 255, 0, 255), (0,0,0))
            drawText(font, 20, 530, f'FIGURE SPEED: {speed:.3f}',(0, 255, 0, 255),(0,0,0))

        pygame.display.flip()
        clock.tick(120)

    glDeleteLists(grid_list, 1)
    glDeleteLists(cube_list, 1)
    pygame.quit()

main()
