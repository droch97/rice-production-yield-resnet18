import os
import rasterio
import numpy as np
from glob import glob
import re

def concatenar_bandas(ruta_entrada, ruta_salida):
    archivos = glob(os.path.join(ruta_entrada, '*.tif'))
    patron = r'(?P<periodo>[^_]+)_(?P<codigo>[^_]+)_(?P<municipio>.+)_(?P<etapa>e[23])_'
    imagenes_dict = {}
    for archivo in archivos:
        nombre = os.path.basename(archivo)
        match = re.match(patron, nombre)
        if match:
            key = (match.group('periodo'), match.group('codigo'))
            etapa = match.group('etapa')
            if key not in imagenes_dict:
                imagenes_dict[key] = {}
            imagenes_dict[key][etapa] = archivo
    for key, etapas in imagenes_dict.items():
        if 'e2' in etapas and 'e3' in etapas:
            with rasterio.open(etapas['e2']) as src1, rasterio.open(etapas['e3']) as src2:
                bandas1 = [src1.read(i) for i in range(1, 6)]
                bandas2 = [src2.read(i) for i in range(1, 6)]
                new_bandas = np.stack(bandas1 + bandas2)
                meta = src1.meta.copy()
                meta.update(count=10)
                nuevo_nombre = f"{key[0]}_{key[1]}.tif"
                ruta_img_salida = os.path.join(ruta_salida, nuevo_nombre)
                with rasterio.open(ruta_img_salida, 'w', **meta) as dst:
                    for i in range(10):
                        dst.write(new_bandas[i], i + 1)
            print(f'Imagen generada: {ruta_img_salida}')

def concatenar_bandas_masivo(ruta_base_entrada, ruta_salida):
    municipios = [d for d in os.listdir(ruta_base_entrada) if os.path.isdir(os.path.join(ruta_base_entrada, d))]
    for municipio in municipios:
        ruta_entrada = os.path.join(ruta_base_entrada, municipio)
        os.makedirs(ruta_salida, exist_ok=True)
        concatenar_bandas(ruta_entrada, ruta_salida)

# Uso:
input_dir_base = '/home/cris/Documents/TESIS/BR_DATA/2024_data/images'
output_dir = '/home/cris/Documents/TESIS/BR_DATA/merge_images'
concatenar_bandas_masivo(input_dir_base, output_dir)

