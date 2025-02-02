#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pathlib import Path
import os
import math
import numpy as np
import argparse
from colorama import init, Fore, Style

init()

rgb_colors = {'blue':[0.0,0.0,1.0,1.0],
              'gray':[0.2,0.2,0.2,1.0],
              'black':[0.0,0.0,0.0,1.0]}

rgb_t = {'blue':[0,0,255],
               'gray':[51,51,51],
               'black':[0,0,0]}


def check_width_value(width):
    val = int(width)
    if val < 800 or val > 1600:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Width value must be less than 1601 and greater than 799."+Fore.RESET+Style.RESET_ALL)
    return val

def check_height_value(height):
    val = int(height)
    if val < 600 or val > 900:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Height value must be less than 901 and greater than 599."+Fore.RESET+Style.RESET_ALL)
    return val

def get_objs():
    extension = '.obj'
    directory = os.getcwd()
    return [file.name for file in Path(directory).glob(f'*{extension}')]

def reset_scene():
    global quaternion, scale, dragging, last_mouse_pos, translation, is_ortho
    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
    scale = 1  # Restablece el zoom
    dragging = False  # Deshabilitar arrastre del ratón
    last_mouse_pos = (0, 0)  # Restablecer posición del ratón
    translation = [0.0, 0.0]  # Restablecer traslación
    is_ortho = False  # Restablecer vista en perspectiva
    #setup_view_perspective(display)  # Restablecer la vista en perspectiva


def check_source_ext(file):
    name, ex = os.path.splitext(file)
    if os.path.exists(file):
        if ex != ".obj":
            raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Source file must be '.obj' ('{ex}' is not valid)."+Fore.RESET+Style.RESET_ALL)
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"FILE NOT FOUND: file or path '{file}' not found."+Fore.RESET+Style.RESET_ALL)
    return file

def load_obj(filename):
    vertices = []
    #edges = []
    edges = set()
    num_edges = 0
    num_verts = 0
    num_triangles = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vértice
                num_verts += 1
                parts = line.strip().split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
            elif line.startswith('f '):  # Cara
                num_triangles += 1
                parts = line.strip().split()
                face_indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                for i in range(len(face_indices)):
                    edges.add(tuple(sorted((face_indices[i], face_indices[(i + 1) % len(face_indices)]))))
                    #edges.append((face_indices[i], face_indices[(i + 1) % len(face_indices)]))
                    num_edges = len(edges)
    return vertices, edges, num_verts, num_triangles, num_edges

def drawText(f, x, y, text, c, bgc):
    textSurface = f.render(text, True, c, bgc)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def show_controls():
    print("\n--------------------- Controls ---------------------")
    
    print("\nKeyboard Controls (Movement):")
    print("  - Up Arrow: Move the scene forward (rotate upwards)")
    print("  - Down Arrow: Move the scene backward (rotate downwards)")
    print("  - Left Arrow: Move the scene left (rotate left)")
    print("  - Right Arrow: Move the scene right (rotate right)")
    
    print("\nRotation Controls:")
    print("  - 'R' Key: Reset the scene rotation and scaling")
    print("  - 'M' Key: Rotate the scene clockwise around the Z-axis")
    print("  - 'N' Key: Rotate the scene counterclockwise around the Z-axis")
    
    print("\nView Mode Toggle:")
    print("  - 'P' Key: Toggle between Orthographic and Perspective views")
    
    print("\nZoom Controls:")
    print("  - 'Z' Key: Zoom in (increase scale)")
    print("  - 'X' Key: Zoom out (decrease scale)")
    print("  - Mouse Wheel: Zoom in/out")

    print("\nTranslation Controls (Drag):")
    print("  - Hold Left Mouse Button: Drag to move the scene")
    
    print("\nMiscellaneous:")
    print("  - 'H' Key: Toggle the visibility of on-screen information (model name, scale, view mode)")
    print("  - ESC Key: Exit the program")
    
    print("\n----------------------------------------------------")

    
# Clase para manejar cuaterniones
class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def to_matrix(self):
        ww, xx, yy, zz = self.w * self.w, self.x * self.x, self.y * self.y, self.z * self.z
        wx, wy, wz = self.w * self.x, self.w * self.y, self.w * self.z
        xy, xz, yz = self.x * self.y, self.x * self.z, self.y * self.z

        return np.array([
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy), 0],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx), 0],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def __mul__(self, other):
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        )

# Función para crear un cuaternión de rotación
def create_rotation_quaternion(angle, x, y, z):
    half_angle = math.radians(angle) / 2.0
    sin_half_angle = math.sin(half_angle)
    return Quaternion(math.cos(half_angle), x * sin_half_angle, y * sin_half_angle, z * sin_half_angle)

# Función para inicializar la proyección ortogonal
def setup_view_ortho(display):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Definir el rango de la proyección ortogonal
    aspect_ratio = display[0] / display[1]
    ortho_size = 10  # Tamaño del área visible en la proyección ortogonal 10
    #glOrtho(-ortho_size * aspect_ratio, ortho_size * aspect_ratio, -ortho_size, ortho_size, -50, 50)
    glOrtho(-ortho_size * 0.5 * aspect_ratio, ortho_size * 0.5 * aspect_ratio, -ortho_size * 0.5, ortho_size * 0.5, -50, 50)

    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glTranslatef(0.0,0.0,-3.0)

def text_pos(h,p):
    inc_total = (h - 600)
    h_pos = p + inc_total
    return h_pos

def check_color(color):
    colors = ['blue','gray','black']
    if color not in colors:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+"Background color must be 'blue', 'gray' or 'black'."+Fore.RESET+Style.RESET_ALL)
    return color

def check_lw(w):
    width = float(w)
    if width < 1.0:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+"Line width must be equal or greater than 1.0."+Fore.RESET+Style.RESET_ALL)
    return width
    
# Función para inicializar la proyección en perspectiva
def setup_view_perspective(display):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, (display[0] / display[1]), 0.1, 80)#50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10.0)

def window(args):
    show_controls()
    list_objects = get_objs()
    #print(list_objects)
    pygame.init()
    
    text_bgR = rgb_t[args.bg_color][0]
    text_bgG = rgb_t[args.bg_color][1]
    text_bgB = rgb_t[args.bg_color][2]

    text_pos1 = text_pos(args.window_height,570)
    text_pos2 = text_pos(args.window_height,550)
    text_pos3 = text_pos(args.window_height,530)
    text_pos4 = text_pos(args.window_height,510)
    text_pos5 = text_pos(args.window_height,490)
    text_pos6 = text_pos(args.window_height,470)
    text_pos7 = text_pos(args.window_height,450)
  
    display = (args.window_width, args.window_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Model Viewer")
    font = pygame.font.SysFont('arial', 15)

    #glEnable(GL_DEPTH_TEST)#######################################################

    #glClearColor(0.0, 0.0, 1.0, 1.0)

    glClearColor(rgb_colors[args.bg_color][0],
                 rgb_colors[args.bg_color][1],
                 rgb_colors[args.bg_color][2],
                 rgb_colors[args.bg_color][3])

    # Cargar el modelo OBJ
    #path = r'C:\Users\Usuario\Documents\fondo\temple_maze.obj'
    path = args.load_object
    model_name = os.path.basename(path)
    vertices, edges, num_verts, num_triangles, num_edges = load_obj(path)
    scale = 1.0
    hide_data = False
    use_quaternions = True

    # Crear la lista de display para el modelo
    model_list = glGenLists(1)
    glNewList(model_list, GL_COMPILE)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glLineWidth(args.line_width)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glEndList()

    # Inicializar la vista en perspectiva por defecto
    is_ortho = False
    setup_view_perspective(display)

    # Inicializar el cuaternión de rotación (sin rotación inicial)
    quaternion = Quaternion(1, 0, 0, 0)

    dragging = False
    last_mouse_pos = (0, 0)
    translation = [0.0, 0.0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                '''if event.key == pygame.K_z:
                    scale += 0.05
                elif event.key == pygame.K_x:
                    scale -= 0.05'''
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    hide_data = not hide_data
                elif event.key == pygame.K_r:
                    quaternion = Quaternion(1, 0, 0, 0)
                    scale = 1
                    dragging = False
                    last_mouse_pos = (0, 0)
                    translation = [0.0, 0.0]
                    is_ortho = False
                    setup_view_perspective(display) # Restablece vista en perspectiva'''
                    
                elif event.key == pygame.K_p:  # Cambiar entre ortogonal y perspectiva
                    is_ortho = not is_ortho
                    if is_ortho:
                        setup_view_ortho(display)
                    else:
                        setup_view_perspective(display)
                        
                elif event.key == pygame.K_t:  # Vista cenital (tecla 't')
                    # Aplicar rotación para la vista cenital
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    #translation = [0.0, 0.0]  # Restablece la traslación
                    #scale = 1  # Restablece el zoom
                    # Rotar la cámara 90 grados sobre el eje X para vista cenital
                    rotation = create_rotation_quaternion(-90, 1, 0, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_b:
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    rotation = create_rotation_quaternion(90, 1, 0, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_j:
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    rotation = create_rotation_quaternion(90, 0, 1, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_l:
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    rotation = create_rotation_quaternion(-90, 0, 1, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_f:
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    rotation = create_rotation_quaternion(0, 0, 1, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_k:
                    quaternion = Quaternion(1, 0, 0, 0)  # Restablece rotación
                    rotation = create_rotation_quaternion(180, 0, 1, 0)
                    quaternion = quaternion * rotation
                elif event.key == pygame.K_q:
                    if use_quaternions:
                        use_quaternions = False
                        quaternion = Quaternion(1, 0, 0, 0)
                        scale = 1
                        dragging = False
                        last_mouse_pos = (0, 0)
                        translation = [0.0, 0.0]
                        is_ortho = False
                        setup_view_perspective(display)
                    else:
                        use_quaternions = True
                        quaternion = Quaternion(1, 0, 0, 0)
                        scale = 1
                        dragging = False
                        last_mouse_pos = (0, 0)
                        translation = [0.0, 0.0]
                        is_ortho = False
                        setup_view_perspective(display)

                    
            elif event.type == pygame.MOUSEWHEEL:  # Rueda ratón
                if event.y > 0:
                    scale += 0.05
                elif event.y < 0:
                    scale -= 0.05
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    translation[0] += dx * 0.01  # Ajusta la velocidad de desplazamiento
                    translation[1] -= dy * 0.01  # Invertir el movimiento vertical
                    last_mouse_pos = (mouse_x, mouse_y)

        key = pygame.key.get_pressed()

        # Rotación con cuaterniones (si se presionan las teclas de dirección)
        if key[pygame.K_UP]:
            if use_quaternions:
                rotation = create_rotation_quaternion(2, 1, 0, 0)
                quaternion = quaternion * rotation
            else:
                glRotatef(2, 1, 0, 0)
        if key[pygame.K_DOWN]:
            if use_quaternions:
                rotation = create_rotation_quaternion(-2, 1, 0, 0)
                quaternion = quaternion * rotation
            else:
                glRotatef(-2, 1, 0, 0)
        if key[pygame.K_RIGHT]:
            if use_quaternions:
                rotation = create_rotation_quaternion(2, 0, 1, 0)
                quaternion = quaternion * rotation
            else:
                glRotatef(2, 0, 1, 0)
        if key[pygame.K_LEFT]:
            if use_quaternions:
                rotation = create_rotation_quaternion(-2, 0, 1, 0)
                quaternion = quaternion * rotation
            else:
                glRotatef(-2, 0, 1, 0)
        if key[pygame.K_m]:
            if use_quaternions:
                rotation = create_rotation_quaternion(-2, 0, 0, 1)
                quaternion = quaternion * rotation
            else:
                glRotatef(-2, 0, 0, 1)
        if key[pygame.K_n]:
            if use_quaternions:
                rotation = create_rotation_quaternion(2, 0, 0, 1)
                quaternion = quaternion * rotation
            else:
                glRotatef(2, 0, 0, 1)
        if key[pygame.K_z]:
            scale -= 0.05
        if key[pygame.K_x]:
            scale += 0.05

        # Limpiar la pantalla y cargar la nueva matriz de rotación
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glTranslatef(translation[0], translation[1], 0)

        # Convertir el cuaternión a matriz de rotación
        rotation_matrix = quaternion.to_matrix()
        glMultMatrixf(rotation_matrix)

        # Dibujar el modelo
        glScalef(scale, scale, scale)
        glCallList(model_list)

        glPopMatrix()

        if not hide_data:
            #inc_total = (args.window_height - 600)
            #h_pos = 570 + inc_total
            drawText(font, 20, text_pos1, f'Model: {model_name}', (0, 255, 0, 255), (text_bgR, text_bgG, text_bgB))
            drawText(font, 20, text_pos2, f'Scale: {round(scale, 2)}', (0, 255, 0, 255), (text_bgR, text_bgG, text_bgB))
            view_mode = "Orthographic" if is_ortho else "Perspective"
            drawText(font, 20, text_pos3, f'View: {view_mode}', (0, 255, 0, 255),(text_bgR, text_bgG, text_bgB))
            drawText(font, 20, text_pos4, f'Nun Verts: {num_verts}',(0, 255, 0, 255),(text_bgR, text_bgG, text_bgB))
            drawText(font, 20, text_pos5, f'Nun Faces: {num_triangles}',(0, 255, 0, 255),(text_bgR, text_bgG, text_bgB))
            drawText(font, 20, text_pos6, f'Num Edges: {num_edges}',(0, 255, 0, 255),(text_bgR, text_bgG, text_bgB))
            drawText(font, 20, text_pos7, f'Quaternions: {use_quaternions}',(0, 255, 0, 255),(text_bgR, text_bgG, text_bgB))

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

def main():
    parser = argparse.ArgumentParser(prog="ModelVisor0.1", conflict_handler='resolve',
                                     description="Show obj models")
    parser.add_argument('-load','--load_object',required=True,type=check_source_ext,help="Obj model to load")
    parser.add_argument('-width','--window_width',type=check_width_value,default=800,help="Widow width")
    parser.add_argument('-height','--window_height',type=check_height_value,default=600,help="Window height")
    parser.add_argument('-bg','--bg_color',type=check_color,default='black',help="Background color")
    parser.add_argument('-lw','--line_width',type=check_lw,default=1.0,help='Line width')

    args = parser.parse_args()
    window(args)
    
if __name__ =="__main__":
    main()
