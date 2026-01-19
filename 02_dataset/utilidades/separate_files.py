import os
import shutil

# Cambia esto por la ruta de tu carpeta con los archivos
input_dir = '/home/cris/Documents/TESIS/BR_DATA/DATASET64/images'
output_dir = '/home/cris/Documents/TESIS/BR_DATA/DATASET64'

# Subcarpetas destino
for sufijo in ['images_e1', 'images_e2', 'images_e3']:
    os.makedirs(os.path.join(output_dir, sufijo), exist_ok=True)

for filename in os.listdir(input_dir):
    src_file = os.path.join(input_dir, filename)
    if not os.path.isfile(src_file):
        continue  # Omitir subcarpetas y directorios
    if '_e1_' in filename:
        destino = os.path.join(output_dir, 'images_e1', filename)
        shutil.copy2(src_file, destino)
    elif '_e2_' in filename:
        destino = os.path.join(output_dir, 'images_e2', filename)
        shutil.copy2(src_file, destino)
    elif '_e3_' in filename:
        destino = os.path.join(output_dir, 'images_e3', filename)
        shutil.copy2(src_file, destino)