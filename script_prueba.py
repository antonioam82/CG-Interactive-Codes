#!/usr/bin/env python
# -*- coding: utf-8 -*-
from load_obj4c5 import load_obj
from itertools import islice
import argparse
import os


def check_item(item):
    items = ['faces','edges','vertices','none']
    if item not in items:
        raise argparse.ArgumentTypeError("Item must be 'faces', 'edges', 'vertices' or 'none'.")
    return item

def check_file(file):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError(f"ERROR: File '{file}' not found")
    return file

def main():
    parser = argparse.ArgumentParser(prog="script_prueba", conflict_handler='resolve',
                                     description="Check obj reading",allow_abbrev=False)
    parser.add_argument('-load','--load_object',required=True,type=check_file,help="Obj model to load")
    parser.add_argument('-item','--show_item',required=True,type=check_item,help="Info to show")
    parser.add_argument('-clr','--color',action='store_true',help='Use color')
    parser.add_argument('-ec','--enable_centering',action='store_true', help='Center model')
    parser.add_argument('-of','--only_first',type=int,default=None,help='item index start')

    args = parser.parse_args()
    if args.show_item == 'faces':
        args.color = True
    try:
        filename = args.load_object
        color = args.color
        v, e, nv, nt, ne, f, pv, le = load_obj(filename,color,args)
        item_ = args.show_item
        long = abs(30-(len(filename)))
        print(f"\n{filename}{'-'*long}")
        print(f"NUM VERTS: {nv}")
        print(f"NUM FACES: {nt}")
        print(f"NUM EDGES: {ne}")
        print(f"POL VERTS: {pv}")
        print(f"LDL ERROR: {le}")
        print('-'*30)
        if item_ != 'none':
            if item_ == 'vertices':
               if args.only_first:
                   print(f'VERTICES:\n{v[:args.only_first]}','...')
               else:
                   print(f'VERTICES:\n{v}')
            elif item_ == 'edges':
                if args.only_first:
                   print(f'EDGES:\n{list(islice(e,args.only_first))}','...')
                else:
                    print(f'EDGES:\n{e}')
            elif item_ == 'faces':
                if args.only_first:
                    print(f'FACES:\n{f[:args.only_first]}','...')
                else:
                    print(f'FACES:\n{f}')
    except Exception as e:
        print(f"UNEXPECTED ERROR: {str(e)}.")

if __name__ =="__main__":
    main()

