#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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
    other_cube_list = glGenLists(1)
    glNewList(other_cube_list, GL_COMPILE)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.4, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(another_cube[vertex])
    glEnd()

    glEndList()
    return other_cube_list

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

# Función para calcular la AABB (Axis-Aligned Bounding Box)
def calculate_aabb(vertices, position):
    min_x = min([vertex[0] + position[0] for vertex in vertices])
    max_x = max([vertex[0] + position[0] for vertex in vertices])
    min_y = min([vertex[1] + position[1] for vertex in vertices])
    max_y = max([vertex[1] + position[1] for vertex in vertices])
    min_z = min([vertex[2] + position[2] for vertex in vertices])
    max_z = max([vertex[2] + position[2] for vertex in vertices])
    return min_x, max_x, min_y, max_y, min_z, max_z

'''def check_collision(aabb1, aabb2):
    # Comprobar si los rangos de las AABBs se solapan en cada eje
    return (aabb1[0] <= aabb2[1] and aabb1[1] >= aabb2[0] and  # Eje X
            aabb1[2] <= aabb2[3] and aabb1[3] >= aabb2[2] and  # Eje Y
            aabb1[4] <= aabb2[5] and aabb1[5]+0.1 >= aabb2[4])     # Eje Z'''

'''def check_collision(aabb_moving, aabb_static, direction):
    # Verificamos si los rangos de las AABBs se solapan en cada eje
    col = (aabb_moving[0] <= aabb_static[1] and aabb_moving[1] >= aabb_static[0] and  # eje X
           aabb_moving[2] <= aabb_static[3] and aabb_moving[3] >= aabb_static[2] and  # eje Y
           aabb_moving[4] <= aabb_static[5] and aabb_moving[5] >= aabb_static[4])     # eje Z

    if not col:
        return None  # No hay colisión
    
    # Calcular el centro de cada AABB (promedio de mínimo y máximo en cada eje)
    center_moving = (
        (aabb_moving[0] + aabb_moving[1]) / 2,
        (aabb_moving[2] + aabb_moving[3]) / 2,
        (aabb_moving[4] + aabb_moving[5]) / 2
    )
    center_static = (
        (aabb_static[0] + aabb_static[1]) / 2,
        (aabb_static[2] + aabb_static[3]) / 2,
        (aabb_static[4] + aabb_static[5]) / 2
    )

    # Definir el vector unitario de la dirección de movimiento
    if direction == 'front':
        mov_vec = (0, 0, 1)
    elif direction == 'back':
        mov_vec = (0, 0, -1)
    elif direction == 'right':
        mov_vec = (1, 0, 0)
    elif direction == 'left':
        mov_vec = (-1, 0, 0)
    else:
        mov_vec = (0, 0, 0)  # En caso de que no se defina una dirección válida

    # Vector que va desde el centro del objeto en movimiento al centro del otro objeto
    diff = (
        center_static[0] - center_moving[0],
        center_static[1] - center_moving[1],
        center_static[2] - center_moving[2]
    )
    
    # Producto punto entre diff y el vector de movimiento
    dot = diff[0] * mov_vec[0] + diff[1] * mov_vec[1] + diff[2] * mov_vec[2]
    print(dot)
    
    if dot > 0:
        return "trasera"   # La colisión ocurre por detras
    else:
        return "frontal"   # La colisión ocurre por delante'''

def check_collision(aabb_moving, aabb_static, direction):
    # 1. Comprobar solapamiento AABB
    col = (aabb_moving[0] <= aabb_static[1] and aabb_moving[1] >= aabb_static[0] and  
           aabb_moving[2] <= aabb_static[3] and aabb_moving[3] >= aabb_static[2] and  
           aabb_moving[4] <= aabb_static[5] and aabb_moving[5] >= aabb_static[4])

    if not col:
        return None

    # 2. Calcular centros
    center_moving = (
        (aabb_moving[0] + aabb_moving[1]) / 2,
        (aabb_moving[2] + aabb_moving[3]) / 2,
        (aabb_moving[4] + aabb_moving[5]) / 2
    )
    center_static = (
        (aabb_static[0] + aabb_static[1]) / 2,
        (aabb_static[2] + aabb_static[3]) / 2,
        (aabb_static[4] + aabb_static[5]) / 2
    )

    # 3. Definir vector de movimiento
    if direction == 'front':
        mov_vec = (0, 0, 1)
    elif direction == 'back':
        mov_vec = (0, 0, -1)
    elif direction == 'right':
        mov_vec = (1, 0, 0)
    elif direction == 'left':
        mov_vec = (-1, 0, 0)
    else:
        mov_vec = (0, 0, 0)

    # 4. Calcular diferencia
    diff = (
        center_static[0] - center_moving[0],
        center_static[1] - center_moving[1],
        center_static[2] - center_moving[2]
    )

    # 5. Decidir tipo de colisión usando ejes principales
    dot = diff[0] * mov_vec[0] + diff[1] * mov_vec[1] + diff[2] * mov_vec[2]

    # Si se mueve en eje Z (frente/atrás)
    if direction in ['front', 'back']:
        if abs(diff[0]) > abs(diff[2]):
            if diff[0] > 0:
                return "lateral derecha"
            else:
                return "lateral izquierda"
        else:
            if dot > 0:
                return "trasera"
            else:
                return "frontal"

    # Si se mueve en eje X (izquierda/derecha)
    if direction in ['left', 'right']:
        if abs(diff[2]) > abs(diff[0]):
            if diff[2] > 0:
                return "frontal"
            else:
                return "trasera"
        else:
            if dot > 0:
                return "lateral derecha"
            else:
                return "lateral izquierda"

    # Caso raro (sin movimiento)
    return "desconocido"



# Variables globales para controlar la rotación
rotation_speed = 2.0  # velocidad de rotación por frame (más baja es más lenta)
target_angle = 0
current_angle = 0
rotating = False

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)
    font = pygame.font.SysFont('arial', 15)
    glRotatef(15, 1, 0, 0)

    cube_list = Cube()
    grid_list = draw_grid()
    other_list = other_cube()
    hide_data = False
    #collision = False
    
    #frontal_collision = False
    #back_collision = False

    show_controls()

    x = 0.00
    z = -2.60#0.00

    x_c = 0.00
    z_c = 0.00

    global current_angle, target_angle, rotating
    speed = 0.1
    speed_c = 0.1
    running = True
    direction = 'front'
    rot = 0
    scene = 0
    index = 0
    directions = ['front', 'right', 'back', 'left']

    while running:
        # Calcular AABBs de los cubos
        aabb_cube = calculate_aabb(vertices, (x_c, 0, z_c))
        aabb_other_cube = calculate_aabb(another_cube, (x, 0, z))

        #col = check_collision(aabb_cube, aabb_other_cube)
        #print(col)

        '''# Comprobar colisión
        if check_collision(aabb_cube, aabb_other_cube):
            print("¡Colisión detectada!")
            collision = True
        else:
            print("No hay colisión.")
            collision = False'''

        tipo_colision = check_collision(aabb_cube, aabb_other_cube, direction)
        
        if tipo_colision:
            print(tipo_colision)
            '''print(f"¡Colisión detectada! Tipo: {tipo_colision}")
            #collision = True
        else:
            print("No hay colisión.")
            #collision = False'''
            
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
        
                    # Restaurar las rotaciones acumuladas
                    glLoadIdentity()  # Resetea las transformaciones
                    gluPerspective(45, (display[0] / display[1]), 0.1, 90.0)  # Reestablece la perspectiva
                    glTranslatef(0.0, 0.0, -10)  # Reestablece la cámara alejada
                    glRotatef(15, 1, 0, 0)

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            if direction == 'front' and z + speed <= (grid_size - 1) and tipo_colision != 'frontal' and tipo_colision != 'lateral derecha':
                z += speed
                z_c -= speed_c
                z_c += speed
            elif direction == 'back' and z - speed >= (-grid_size + 1) and tipo_colision != 'frontal' and tipo_colision != 'lateral derecha' :
                z -= speed
                z_c += speed_c
                z_c -= speed
            elif direction == 'right' and x - speed >= (-grid_size + 1) and tipo_colision != 'frontal' and tipo_colision != 'lateral derecha':
                x -= speed
                x_c += speed_c
                x_c -= speed##########################'''
            elif direction == 'left' and x + speed <= (grid_size - 1) and tipo_colision != 'frontal' and tipo_colision != 'lateral derecha' :
                x += speed
                x_c -= speed_c
                x_c += speed
            
        if key[pygame.K_DOWN]:
            if direction == 'front' and z + speed <= (grid_size - 1) and tipo_colision != 'trasera' and tipo_colision != 'lateral izquierda': 
                z -= speed
                z_c += speed_c
                z_c -= speed
            elif direction == 'back' and z + speed <= (grid_size - 1) and tipo_colision != 'trasera' and tipo_colision != 'lateral izquierda':
                z += speed
                z_c -= speed_c
                z_c += speed
            elif direction == 'right' and x - speed >= (-grid_size + 1) and tipo_colision != 'tarsera' and tipo_colision != 'lateral izquierda': 
                x += speed
                x_c -= speed_c
                x_c += speed
            elif direction == 'left' and x + speed <= (grid_size - 1) and tipo_colision != 'trasera' and tipo_colision != 'lateral izquierda':
                x -= speed
                x_c += speed_c
                x_c -= speed

        if key[pygame.K_y]:
            glRotatef(1, 0, -0.1, 0)
        elif key[pygame.K_r]:
            glRotatef(1, 0, 0.1, 0)
        elif key[pygame.K_q]:
            glRotatef(1, -0.1, 0, 0)
        elif key[pygame.K_w]:
            glRotatef(1, 0.1, 0, 0)
        

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

        # Dibujar el grid
        glPushMatrix()
        glTranslatef(x, 0.00, z)
        glCallList(grid_list)
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0) #2.6
        glRotatef(rot,0,1,0)
        glCallList(other_list)
        glPopMatrix()
        glPopMatrix()

        # Dibujar el cubo
        glPushMatrix()
        glTranslatef(x_c, 0.0, z_c)
        glRotatef(-current_angle, 0, 1, 0)
        glCallList(cube_list)
        glPopMatrix()

        #rot += 1

        spd = round(speed, 3)
        spdc = round(speed_c, 3)

        if not hide_data:
            drawText(font, 20, 570, f'DIRECTION: {direction}', (0, 255, 0, 255), (0, 0, 0))
            drawText(font, 20, 550, f'CAMERA SPEED: {spd}', (0, 255, 0, 255), (0, 0, 0))
            drawText(font, 20, 530, f'FIGURE SPEED: {spdc}', (0, 255, 0, 255), (0, 0, 0))

        glFlush()
        pygame.display.flip()
        pygame.time.wait(10)

main()
pygame.quit()
