import argparse



def load_obj(args):
    vertices: list[list[float]] = []
    faces: list[list[int]] = []
    edges: set[tuple[int, int]] = set()
    num_verts: int = 0
    num_triangles: int = 0
    num_edges: int = 0
    polygon_verts: int = 0
    load_error: bool = False
    print(args.load_object)

    try:
        with open(args.load_object, 'r') as file:

            for line in file:
               #print(line)
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()

                # VERTICES
                if parts[0] == 'v':
                    if len(parts) < 4:
                        continue

                    vertex = [
                        float(parts[1]),
                        float(parts[2]),
                        float(parts[3])
                    ]
                    vertices.append(vertex)
                    num_verts += 1

                # FACES
                elif parts[0] == 'f':

                    face_indices: list[int] = []
                    for part in parts[1:]:

                        # soporta v, v/vt, v//vn, v/vt/vn
                        vals = part.split('/')
                        if vals[0] == '':
                            continue
                        idx = int(vals[0])

                        # soporte índices negativos OBJ
                        if idx < 0:
                            idx = len(vertices) + idx
                        else:
                            idx -= 1
                        face_indices.append(idx)

                    if len(face_indices) < 4:
                        continue

                    polygon_verts = len(face_indices)

                    if args.color:
                        faces.append(face_indices)

                    num_triangles += 1

                    # generar edges
                    for i in range(len(face_indices)):
                        v1 = face_indices[i]
                        v2 = face_indices[(i + 1) % len(face_indices)]
                        edges.add(tuple(sorted((v1, v2))))

        num_edges = len(edges)
        print(num_edges)

        # CENTERING
        '''if args.enable_centering and vertices:
            verts_np = np.array(vertices)
            min_v = np.min(verts_np, axis=0)
            max_v = np.max(verts_np, axis=0)
            center = (min_v + max_v) / 2.0

            vertices = [list(np.array(v) - center) for v in vertices]'''

    except Exception as e:
        print(f'ERROR: {str(e)}')
        load_error = True
    print('\n-----------------------------')
    print(f'NV: {num_verts}')
    print(f'NF: {num_triangles}')
    print('-----------------------------\n')
    #print("OK!")
    item_ = args.show_item
    if item_ == 'vertices':
        print('VERTICES:')
        print(vertices)
    elif item_ == 'edges':
        print('EDGES:')
        print(edges)
    elif item_ == 'faces':
        print('FACES:')
        print(faces)
    #return vertices, edges, num_verts, num_triangles, num_edges, faces, polygon_verts, load_error


def main():
    parser = argparse.ArgumentParser(prog="script_prueba", conflict_handler='resolve',
                                     description="Check obj reading",allow_abbrev=False)
    parser.add_argument('-load','--load_object',required=True,type=str,help="Obj model to load")
    parser.add_argument('-item','--show_item',required=True,type=str,help="Info to show")
    parser.add_argument('-clr','--color',action='store_true',help='Use color')

    args = parser.parse_args()
    load_obj(args)

if __name__ =="__main__":
    main()
