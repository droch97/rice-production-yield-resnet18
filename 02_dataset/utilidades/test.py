import rasterio

ruta_archivo = '/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/images/1920_4301636_0_0.tif'

with rasterio.open(ruta_archivo) as src:
    cantidad_bandas = src.count

print(f'El archivo tiene {cantidad_bandas} bandas')