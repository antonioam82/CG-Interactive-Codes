import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import math
import numpy as np
import argparse
from colorama import init, Fore, Style

init()

def check_width_value(width):
    val = int(width)
    if val < 800 or val > 1600:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Width value must be less than 1600 and greater than 799."+Fore.RESET+Style.RESET_ALL)
    return val

def check_height_value(height):
    val = int(height)
    if val < 600 or val > 900:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Height value must be less than 900 and greater than 600."+Fore.RESET+Style.RESET_ALL)
    return val

def check_source_ext(file):
    name, ex = os.path.splitext(file)
    if os.path.exists(file):
        if ex != ".obj":
            raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"Source file must be '.obj' ('{ex}' is not valid)."+Fore.RESET+Style.RESET_ALL)
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"FILE NOT FOUND: file or path '{file}' not found."+Fore.RESET+Style.RESET_ALL)
    return file

def main():
    parser = argparse.ArgumentParser(prog="ModelVisor0.1", conflict_handler='resolve',
                                     description="Show obj models")
    parser.add_argument('-load','--load_object',required=True,type=check_source_ext,help="Obj model to load")
    parser.add_argument('-width','--window_width',type=check_width_value,default=800,help="Widow width")
    parser.add_argument('-height','--window_height',type=check_height_value,default=600,help="Window height")

    args = parser.parse_args()
    print(args.window_width)
    print(args.window_height)


    
if __name__ =="__main__":
    main()
