import os
import numpy as np
import rasterio
import pandas as pd

# input_root = "/home/cris/Documents/TESIS/BR_DATA/2024_data"
input_root = "/home/cris/Documents/TESIS/BR_DATA/merge_images"
output_img_dir = "/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/images"
output_csv = "/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/info.csv"
tile_size = 64

os.makedirs(output_img_dir, exist_ok=True)
data_records = []

for root, dirs, files in os.walk(input_root):
    for file in files:
        if not file.endswith('.tif'):
            continue
        tif_path = os.path.join(root, file)
        
        municipio = os.path.basename(root)
        print(municipio)
        with rasterio.open(tif_path) as src:
            img = src.read()
            channels, height, width = img.shape
            tiles_x = (width + tile_size - 1) // tile_size
            tiles_y = (height + tile_size - 1) // tile_size

            for ty in range(tiles_y):
                for tx in range(tiles_x):
                    x0 = tx * tile_size
                    y0 = ty * tile_size
                    x1 = min(x0 + tile_size, width)
                    y1 = min(y0 + tile_size, height)
                    tile = img[:, y0:y1, x0:x1]

                    pad_x = tile_size - (x1 - x0)
                    pad_y = tile_size - (y1 - y0)
                    if pad_x > 0 or pad_y > 0:
                        pad_width = ((0,0), (0, pad_y), (0, pad_x))
                        tile = np.pad(tile, pad_width, mode='constant', constant_values=0)
                    
                    tile_filename = f"{os.path.splitext(file)[0]}_{tx}_{ty}.tif"
                    tile_path = os.path.join(output_img_dir, tile_filename)

                    profile = src.profile.copy()
                    profile.update(
                        height=tile_size,
                        width=tile_size,
                        transform=rasterio.windows.transform(
                            rasterio.windows.Window(x0, y0, tile_size, tile_size),
                            src.transform
                        )
                    )
                    with rasterio.open(tile_path, 'w', **profile) as dst:
                        dst.write(tile)
                    
                    # Extraer las primeras 4 bandas (índices 0 a 3)
                    bands_1_to_4 = tile[0:4, :, :]

                    # Máscara que verifica si todas las 4 bandas son cero o NaN en cada píxel
                    mask_bandas_cero = np.all((bands_1_to_4 == 0) | np.isnan(bands_1_to_4), axis=0)

                    # Máscara válida para ROI: píxeles que NO tienen las 4 bandas cero simultáneamente
                    valid_mask = ~mask_bandas_cero

                    # Cálculo del porcentaje
                    valid_pixels = np.sum(valid_mask)
                    total_pixels = tile.shape[1] * tile.shape[2]  # altura x ancho del tile
                    roi_percentage = 100 * valid_pixels / total_pixels

                    data_records.append({
                        'filename': tile_filename,
                        'label': municipio,
                        'roi_fraction': roi_percentage
                    })


df_new = pd.DataFrame(data_records)

if os.path.exists(output_csv):
    df_existing = pd.read_csv(output_csv)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['filename'])
    df_combined.to_csv(output_csv, index=False)
else:
    df_new.to_csv(output_csv, index=False)
