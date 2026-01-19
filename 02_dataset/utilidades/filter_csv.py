import pandas as pd
import os

def filtrar_por_umbral(input_csv, umbral):
    # Cargar archivo CSV
    df = pd.read_csv(input_csv)
    
    # Filtrar filas donde roi_fraction sea mayor o igual al umbral
    df_filtrado = df[df['roi_fraction'] >= umbral]
    
    # Construir nuevo nombre de archivo con sufijo _umbral antes de la extensión
    base, ext = os.path.splitext(input_csv)
    nuevo_nombre = f"{base}_final{ext}"
    
    # Guardar archivo filtrado
    df_filtrado.to_csv(nuevo_nombre, index=False)
    print(f"Archivo filtrado guardado como: {nuevo_nombre}")

# Ejemplo de uso:
filtrar_por_umbral('/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/file_labeled.csv', 1)
