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
