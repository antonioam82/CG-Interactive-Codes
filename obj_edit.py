import os


def convertir_obj_para_funcion(input_obj, output_obj):
    with open(input_obj, 'r') as fin, open(output_obj, 'w') as fout:
        for line in fin:
            line = line.strip()

            # Mantener SOLO vértices
            if line.startswith('v '):
                fout.write(line + '\n')

            # Mantener SOLO caras con índices simples
            elif line.startswith('f '):
                parts = line.split()
                indices = []

                for p in parts[1:]:
                    # Convierte "12/5/9" -> "12"
                    # Convierte "12//9"  -> "12"
                    # Convierte "12"     -> "12"
                    idx = p.split('/')[0]

                    # Seguridad extra: ignorar basura
                    if idx.isdigit():
                        indices.append(idx)

                # Escribir solo si la cara es válida
                if len(indices) >= 3:
                    fout.write('f ' + ' '.join(indices) + '\n')

convertir_obj_para_funcion(
    "cube.obj",
    "cube_edited.obj"
)
