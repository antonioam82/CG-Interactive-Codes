import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertextxt = "C:\\Users\\Antonio\\Documents\\docs\\vertices.txt"
facestxt = "C:\\Users\\Antonio\\Documents\\docs\\faces.txt"

paints = [
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 255, 255)
]

def get_list(txtname):
    listname = []
    with open(txtname) as f:
        for line in f:
            line = line.strip().rstrip(",\r\n").replace("(", "").replace(")", "")
            row = list(line.split(","))
            listname.append(row)
    listname = [[float(j) for j in i] for i in listname]
    return listname

modelVerts = get_list(vertextxt)
modelFaces = get_list(facestxt)

# Para depuración, imprime los primeros elementos de las listas
print("Model Vertices:", modelVerts[:5])
print("Model Faces:", modelFaces[:5])

def drawfaces():
    glClear(GL_COLOR_BUFFER_BIT or GL_DEPHT_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for eachface in (modelFaces):
        color = 2
        for eachvert in eachface:
            color += 1
            if color >5:
                color = 0
            glColor3fv(paints[color])
            glVertex3fv(modelVerts[int(eachvert)])
    glEnd()

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_caption("RENDERING OBJECT")
    FPS = pygame.time.Clock()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45,1,.1,50)
    glTranslate(0,-1,-5)
    glRotate(0,1,0,0)

    Left = False
    Right = False

    def moveOBJ():
        if Left:
            glRotate(-1,0,1,0)
        if Right:
             glRotate(1,0,1,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    Left = True
                if event.key == K_d:
                    Right = True
            if event.type == KEYUP:
                if event.key == K_a:
                    Left = False
                if event.key == K_d:
                    Right = False

        pygame.display.flip()
        drawfaces()
        moveOBJ()
        FPS.tick(60)
main()
