import pandas as pd

input_csv = '/home/cris/Documents/TESIS/BR_DATA/DATASET64/file_labeled_final.csv'
output_dir = '/home/cris/Documents/TESIS/BR_DATA/DATASET64'  # Cambia por tu carpeta deseada

df = pd.read_csv(input_csv)

# Filtrar y guardar para e1
df_e1 = df[df['filename'].str.contains('_e1_')]
df_e1.to_csv(f'{output_dir}/e1.csv', index=False)

# Filtrar y guardar para e2
df_e2 = df[df['filename'].str.contains('_e2_')]
df_e2.to_csv(f'{output_dir}/e2.csv', index=False)

# Filtrar y guardar para e3
df_e3 = df[df['filename'].str.contains('_e3_')]
df_e3.to_csv(f'{output_dir}/e3.csv', index=False)
