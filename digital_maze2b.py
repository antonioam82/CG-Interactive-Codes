#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import math as m
import sys
import random

#JUST A 3D MAZE DEMO

win_width, win_height = (1100, 600)# (1600, 870)#(1598,870)#(1600, 900)
fps = 165 # 165hz monitor btw the way
#color = [203,232,200]
display = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Raycasting")
clock = pygame.time.Clock()
#active_run = False
random_num = random.randint(1000000000000,9999999999999)

pygame.init()
text_font = pygame.font.SysFont("monospace",15)

'''environment = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]'''
environment = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
[1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
    
fov = 90
xpos, ypos = (1, 1)
rot_r = 0

sensitivity = m.pi/256
move_speed = 0.01

precision = 0.02

wk, sk, ak, dk = False, False, False, False

def make_change():
    global environment
    ran1 = random.randint(1,13)
    ran2 = random.randint(1,13)
    
    if environment[ran1][ran2] == 1:
        environment[ran1][ran2] = 0
    else:
        environment[ran1][ran2] = 1

def active_run_controler():
    global active_run
    if active_run == True:
        active_run = False
    else:
        active_run = True

run = True
counter = 0
apply_changes = False
while run == True:
    
    if apply_changes:
        counter += 1
        if counter == 80:
            print(counter)
            make_change()
            counter = 0
        
    clock.tick(fps)
    pygame.display.update()
    pygame.display.set_caption("Raycasting - FPS: " + str(round(clock.get_fps())))
    

    for e in pygame.event.get():
        if e.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()
        
        if e.type == KEYDOWN:
            if e.key == pygame.K_w:
                wk = True
            if e.key == pygame.K_s:
                sk = True
            if e.key == pygame.K_a:
                ak = True
            if e.key == pygame.K_d:
                dk = True
        if e.type == KEYUP:
            if e.key == pygame.K_w:
                wk = False
            if e.key == pygame.K_s:
                sk = False
            if e.key == pygame.K_a:
                ak = False
            if e.key == pygame.K_d:
                dk = False
            if e.key == pygame.K_z:
                active_run_controler()
            if e.key == pygame.K_g:
                if apply_changes == True:
                    apply_changes = False
                else:
                    apply_changes = True

    x, y = (xpos, ypos)

    
    if wk == True:
        x, y = (x+move_speed*m.cos(rot_r), y+move_speed*m.sin(rot_r))
    if sk == True:
        x, y = (x-move_speed*m.cos(rot_r), y-move_speed*m.sin(rot_r))
    if ak == True:
        rot_r -= sensitivity
    if dk == True:
        rot_r += sensitivity
    if environment[int(x)][int(y)] == 0:
        xpos, ypos = (x, y)

    display.fill((0, 0, 0))
    #display.fill(color)

    for i in range(fov+1):
        rot_d = rot_r + m.radians(i - fov/2)
        x, y = (xpos, ypos)
        sin, cos = (precision*m.sin(rot_d), precision*m.cos(rot_d))
        j = 0
        while True:
            x, y = (x + cos, y + sin)
            j += 1
            #print(environment[int(x)][int(y)])
            if environment[int(x)][int(y)] != 0:
                
                tile = environment[int(x)][int(y)]
                d = j
                j = j * m.cos(m.radians(i-fov/2))
                height = (10/j * 2500)
                break
        if d/2 > 255:
            d = 510
        pygame.draw.line(display,
                         (255-d/2, 255-d/2, 255-d/2), # color
                         (i*(win_width/fov), (win_height/2) + height), # pos 1
                         (i*(win_width/fov), (win_height/2) - height), # pos 2
                         width=int(win_width/fov))
        
    text1 = text_font.render("(x,y)=("+str(x)+","+str(y)+")",1,(255,0,0))
    display.blit(text1,(30,10))
    active_run = random.choice([False,True])
    if active_run == True:
        random_num = random.randint(1000000000000,9999999999999)
    text2 = text_font.render("RUN_VLA: {}".format(str(random_num)),1,(255,0,0))
    display.blit(text2,(30,35))
