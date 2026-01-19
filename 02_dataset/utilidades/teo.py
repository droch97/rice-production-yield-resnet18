import pandas as pd
import os

# Rutas de los archivos CSV
stats_file = '/home/cris/Documents/TESIS/BR_DATA/stats_images_1.csv'
rendimientos_dir = '/home/cris/Documents/TESIS/BR_DATA/rendimientos/'  # Directorio con los archivos de rendimiento
output_file = '/home/cris/Documents/TESIS/BR_DATA/stats_images_con_rendimiento.csv'

# Leer el archivo de estadísticas
df_stats = pd.read_csv(stats_file)

# Crear un diccionario para almacenar todos los rendimientos
rendimientos_dict = {}

# Recorrer todos los archivos en el directorio de rendimientos
for filename in os.listdir(rendimientos_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(rendimientos_dir, filename)
        print(f"Procesando archivo: {filename}")

        # Leer el archivo de rendimiento actual
        df_rendimientos = pd.read_csv(filepath)

        # Crear un diccionario temporal con los rendimientos del archivo actual
        temp_rendimientos_dict = pd.Series(df_rendimientos.rendimiento_kg_ha.values, index=df_rendimientos.codigo_municipio).to_dict()

        # Actualizar el diccionario principal con los rendimientos del archivo actual
        rendimientos_dict.update(temp_rendimientos_dict)

# Función para obtener el rendimiento basado en el código de municipio
def get_rendimiento(mun_code):
    codigo_municipio = f"1920_{mun_code}"
    return rendimientos_dict.get(codigo_municipio, None)

# Aplicar la función para crear la nueva columna 'rendimiento_kg_ha'
df_stats['rendimiento_kg_ha'] = df_stats['mun_code'].apply(get_rendimiento)

# Guardar el DataFrame resultante en un nuevo CSV
df_stats.to_csv(output_file, index=False)

print(f"Archivo guardado con éxito en: {output_file}")