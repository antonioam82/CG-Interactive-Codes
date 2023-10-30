import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

grid_size = 90#120
grid_spacing = 1

def draw_grid():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,1.0)#(0.5, 0.5, 0.5)  # Color gris

    for x in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(x, 0, -grid_size)
        glVertex3f(x, 0, grid_size)

    for z in range(-grid_size, grid_size + 1, grid_spacing):
        glVertex3f(-grid_size, 0, z)
        glVertex3f(grid_size, 0, z)

    glEnd()

verticies = [
    [1, 0, -1],    
    [1, 0.5, -1],    
    [-1, 0.5, -1],      
    [-1, 0, -1],   
    [1, 0, 1],     
    [1, 0.5, 1],     
    [-1, 0, 1],    
    [-1, 0.5, 1]     
    ]

verticies2 = [
    [1, 0, -5],    # inf, der, tras
    [1, 0.5, -5],  # sup, der, tras
    [-1, 0.5, -5], # sup, izq, tras
    [-1, 0, -5],   # inf, izq, tras
    [1, 0, -3],    # inf, der, del
    [1, 0.5, -3],  # sup, der, del
    [-1, 0, -3],   # inf, izq, del
    [-1, 0.5, -3]  # sup, izq, del
    ]

verticies3 = [
    [5, 0, -1],    
    [5, 0.5, -1],    
    [3, 0.5, -1],      
    [3, 0, -1],   
    [5, 0, 1],     
    [5, 0.5, 1],     
    [3, 0, 1],    
    [3, 0.5, 1]     
    ]

verticies4 = [
    [-3, 0, -1],    
    [-3, 0.5, -1],    
    [-5, 0.5, -1],      
    [-5, 0, -1],   
    [-3, 0, 1],     
    [-3, 0.5, 1],     
    [-5, 0, 1],    
    [-5, 0.5, 1]     
    ]

verticies5 = [
    [1, 0, 3],    
    [1, 0.5, 3],    
    [-1, 0.5, 3],      
    [-1, 0, 3],   
    [1, 0, 5],     
    [1, 0.5, 5],     
    [-1, 0, 5],    
    [-1, 0.5, 5]     
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
def Cube_contours():
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()

def Cube_contours2():
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies2[vertex])
    glEnd()

def Cube_contours3():
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies3[vertex])

    glEnd()

def Cube_contours4():
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies4[vertex])
    glEnd()

def Cube_contours5():
    glLineWidth(0.5)
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,0.0)
    for edge in edges:  
        x=0
        for vertex in edge:
            x+=1
            glVertex3fv(verticies5[vertex])
    glEnd()

def random_color():
    r = random.randint(0,1)
    g = random.randint(0,1)
    b = random.randint(0,1)
    return r, g, b

def Cube2():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    r,g,b = random_color()
    glColor3f(r, g, b)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies2[vertex])
    glEnd()

def Cube3():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    r,g,b = random_color()
    glColor3f(r, g, b)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies3[vertex])
    glEnd()

def Cube4():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    r,g,b = random_color()
    glColor3f(r, g, b)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies4[vertex])
    glEnd()

def Cube5():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    glBegin(GL_QUADS)
    r,g,b = random_color()
    glColor3f(r, g, b)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            glVertex3fv(verticies5[vertex])
    glEnd()

# DIBUJA CUBO 
def Cube():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    #glCullFace(GL_BACK)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.1)
    #glColor4f(0.0, 0.0, 0.1, 0.8)
    for surface in surfaces: 
        x=0
        for vertex in surface:
            x+=1
            #glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

# FUNCIÓN PRINCIPAL
def main():
    pygame.init()
    display = (800, 600)#(800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    rot = False
    glClearColor(0.62, 0.62, 0.62, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -7.0)
    glRotatef(27.1, 1, 0, 0)
    
    running = True
    while (running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        key = pygame.key.get_pressed()

        if key[pygame.K_p]:
            rot = True
        elif key[pygame.K_s]:
            rot = False
            
        # ROTACIONES
        if key[pygame.K_UP]:
            glRotatef(0.1, -1, 0, 0)       
        if key[pygame.K_DOWN]:
            glRotatef(0.1, 1, 0, 0)
            
        if rot == True:
            glRotatef(1, 0, 1, 0)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        Cube()
        Cube2()
        Cube3()
        Cube4()
        Cube5()
        Cube_contours()
        Cube_contours2()
        Cube_contours3()
        Cube_contours4()
        Cube_contours5()
    
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.quit()
         
main()
