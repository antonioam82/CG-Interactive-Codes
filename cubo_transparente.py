import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Vertices del cubo
vertices = [
    [ 1,-1,-1], [ 1,1,-1], [-1,1,-1], [-1,-1,-1],
    [ 1,-1, 1], [ 1,1, 1], [-1,-1, 1], [-1,1, 1]
]

# Conexiones (edges)
edges = (
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,7),(7,6),(6,4),
    (0,4),(1,5),(2,7),(3,6)
)

# Caras (surfaces)
surfaces = (
    (0,1,2,3),(4,5,7,6),(0,1,5,4),
    (2,3,6,7),(1,2,7,5),(0,3,6,4)
)

# Transparencia inicial
alpha = 0.4  

def draw_cube(alpha):
    # --- Caras transparentes ---
    glEnable(GL_DEPTH_TEST)
    glBegin(GL_QUADS)
    glColor4f(0.2, 0.6, 1.0, alpha)
    for face in surfaces:
        for vert in face:
            glVertex3fv(vertices[vert])
    glEnd()

    # --- Líneas detrás (Depth Test OFF, alpha inversa) ---
    glDisable(GL_DEPTH_TEST)
    glLineWidth(2)
    glBegin(GL_LINES)
    back_line_alpha = max(0.0, 1.0 - alpha)  # más opaco cubo → líneas detrás más tenues
    glColor4f(1, 1, 1, back_line_alpha)
    for edge in edges:
        for vert in edge:
            glVertex3fv(vertices[vert])
    glEnd()

    # --- Líneas delanteras (Depth Test ON, opacas) ---
    glEnable(GL_DEPTH_TEST)
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor4f(1, 1, 1, 1.0)
    for edge in edges:
        for vert in edge:
            glVertex3fv(vertices[vert])
    glEnd()

def main():
    global alpha
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    gluPerspective(45, display[0]/display[1], 0.1, 50)
    glTranslatef(0,0,-7)

    clock = pygame.time.Clock()

    print("Controles:")
    print("[+] Aumentar opacidad (hasta 1.0)")
    print("[-] Reducir opacidad (hasta 0.0)")
    print("Flechas: Rotar cubo")
    print("Esc: Salir")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit(); sys.exit()

                if event.key == K_PLUS or event.key == K_EQUALS:
                    alpha = min(1.0, alpha + 0.05)
                    print("Alpha =", round(alpha,2))

                if event.key == K_MINUS:
                    alpha = max(0.0, alpha - 0.05)
                    print("Alpha =", round(alpha,2))

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:  glRotatef(1,0,1,0)
        if keys[K_RIGHT]: glRotatef(1,0,-1,0)
        if keys[K_UP]:    glRotatef(1,1,0,0)
        if keys[K_DOWN]:  glRotatef(1,-1,0,0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(alpha)

        pygame.display.flip()
        clock.tick(60)

main()
