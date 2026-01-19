import pandas as pd

# Rutas de los archivos CSV
stats_file = '/home/cris/Documents/TESIS/BR_DATA/stats_images_1.csv'
rendimientos_dir = '/home/cris/Documents/TESIS/BR_DATA/rendimientos/'  # Directorio con los archivos de rendimiento
output_file = '/home/cris/Documents/TESIS/BR_DATA/stats_images_con_rendimiento.csv'

# input_csv = '/home/cris/Documents/TESIS/BR_DATA/DATASET64/file_labeled_final.csv'
# output_dir = '/home/cris/Documents/TESIS/BR_DATA/DATASET64'  # Cambia por tu carpeta deseada

input_csv = '/home/cris/Documents/TESIS/BR_DATA/output/stadistica_tif.csv'
output_dir = '/home/cris/Documents/TESIS/BR_DATA/output'  # Cambia por tu carpeta deseada

df = pd.read_csv(input_csv)

# Filtrar y guardar para e1
df_e1 = df[df['file_name'].str.contains('_e1_')]
df_e1.to_csv(f'{output_dir}/estadistica_compuestas_e1.csv', index=False)

# Filtrar y guardar para e2
df_e2 = df[df['file_name'].str.contains('_e2_')]
df_e2.to_csv(f'{output_dir}/estadisticas_compuestas_e2.csv', index=False)

# Filtrar y guardar para e3
df_e3 = df[df['file_name'].str.contains('_e3_')]
df_e3.to_csv(f'{output_dir}/estadisticas_compuestas_e3.csv', index=False)
