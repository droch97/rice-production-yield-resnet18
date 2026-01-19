import rasterio
import os
import numpy as np
import pandas as pd
from scipy import stats
import geopandas as gpd
from rasterio.features import rasterize


def getStatsFromTif(imagen_path, geojson_path, output_folder):
    # Leer imagen y metadata
    with rasterio.open(imagen_path) as src:
        bands = src.read()  # (6, alto, ancho)
        meta = src.meta.copy()
    
    # Leer ROI desde GeoJSON
    gdf = gpd.read_file(geojson_path)
    
    # Rasterizar ROI para crear máscara booleana
    mask_roi = rasterize(
        [(geom, 1) for geom in gdf.geometry],
        out_shape=(src.height, src.width),
        transform=src.transform,
        fill=0,
        dtype='uint8'
    ).astype(bool)
    
    # Extraer bandas e máscara de nubes
    red, green, blue, nir, ndvi, cloud_mask = bands[0], bands[1], bands[2], bands[3], bands[4], bands[5]
    
    # Máscara de píxeles válidos dentro de ROI y fuera de nube
    mask_nube = cloud_mask == 0
    
    # Máscaras combinadas
    mask_roi_only = mask_roi
    mask_roi_libre_nubes = mask_roi & mask_nube
    
    # Inicializar diccionario para resultados
    stats_dict = {
        'file_name': os.path.basename(imagen_path),
        'mun_code': os.path.basename(geojson_path).replace('.geojson', '').split('_')[1],
        'mun_name': ' '.join(os.path.basename(geojson_path).replace('.geojson', '').split('_')[2:]),
        'date': '-'.join(os.path.basename(imagen_path.replace('.tif', '')).split('_')[-3:]),  # Asumiendo formato nombre_archivo_fecha.tif
        'total_pixel': red.size,
        'total_pixel_roi': np.sum(mask_roi),
        'ha_total_roi': np.sum(mask_roi) * 0.01,
        'ha_total_roi_nocloud': (np.sum(mask_roi) - np.sum(cloud_mask))* 0.01,
    }
    
    bandas = [red, green, blue, nir, ndvi]
    name_bandas = ['red', 'green', 'blue', 'nir', 'ndvi']
    
    for idx, banda in enumerate(bandas):
        vals_roi = banda[mask_roi_only]
        vals_roi_nocloud = banda[mask_roi_libre_nubes]
        
        stats_dict[f'{name_bandas[idx]}_mean'] = np.mean(vals_roi)
        stats_dict[f'{name_bandas[idx]}_median'] = np.median(vals_roi)
        stats_dict[f'{name_bandas[idx]}_mode'] = stats.mode(vals_roi, nan_policy='omit').mode.item()
        
        stats_dict[f'{name_bandas[idx]}_mean_nocloud'] = np.mean(vals_roi_nocloud)
        stats_dict[f'{name_bandas[idx]}_median_nocloud'] = np.median(vals_roi_nocloud)
        stats_dict[f'{name_bandas[idx]}_mode_nocloud'] = stats.mode(vals_roi_nocloud, nan_policy='omit').mode.item()
    
    os.makedirs(output_folder, exist_ok=True)
    name_csv = 'stats_images.csv'  # Archivo único para todas las imágenes
    output_path = os.path.join(output_folder, name_csv)
    
    df = pd.DataFrame([stats_dict])
    import matplotlib.pyplot as plt

    if os.path.exists(output_path):
        df_existente = pd.read_csv(output_path)
        df_combinado = pd.concat([df_existente, df], ignore_index=True)
        df_combinado.to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)
    
    print(f'Estadísticas agregadas en {output_path}')


base_path = '/home/cris/Documents/TESIS/BR_DATA/2020_data'
images_root = os.path.join(base_path, 'images')
geojson_root = os.path.join(base_path, 'geojson')
output_folder = os.path.join('/home/cris/Documents/TESIS/BR_DATA', 'output')

for subdir in os.listdir(images_root):
    subdir_path = os.path.join(images_root, subdir)
    if os.path.isdir(subdir_path):
        # Buscar el .tif en esa subcarpeta
        tif_files_list = [f for f in os.listdir(subdir_path) if f.endswith('.tif')]
        for tif_files in tif_files_list:
            tif_path = os.path.join(subdir_path, tif_files)  # asumiendo una por carpeta
            # Buscar el .geojson en la carpeta geojson con mismo nombre
            geojson_path = os.path.join(geojson_root, subdir + '.geojson')
            if 'compuesto' in tif_files:
                continue  # Saltar archivos compuestos
            if os.path.exists(geojson_path):
                print(f'Procesando {tif_path} con ROI {geojson_path}')
                getStatsFromTif(tif_path, geojson_path, output_folder)
            else:
                print(f'GeoJSON no encontrado para {subdir}')
