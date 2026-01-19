import pandas as pd

file_in = '/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/info.csv'
merge_out = '/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/file_labeled.csv'

# Cargar archivo base CSV con filename, label, roi_fraction
df_archivos = pd.read_csv(file_in)

# Función para extraer codigo_municipio del label
def extraer_codigo_municipio(label):
    partes = label.split('_')
    if len(partes) >= 2:
        return partes[0] + '_' + partes[1]
    else:
        return None

# Crear columna temporal codigo_municipio en df_archivos
df_archivos['codigo_municipio'] = df_archivos['filename'].apply(extraer_codigo_municipio)

# Función para actualizar 'label' con rendimiento de un CSV dado
def actualizar_label_con_rendimiento(df_archivos, ruta_csv_rendimientos):
    df_rend = pd.read_csv(ruta_csv_rendimientos)
    df_merge = df_archivos.merge(df_rend[['codigo_municipio', 'rendimiento_kg_ha']],
                                on='codigo_municipio',
                                how='left')
    # Actualizar donde rendimiento_kg_ha no es nulo
    mask = df_merge['rendimiento_kg_ha'].notnull()
    df_archivos.loc[mask, 'label'] = df_merge.loc[mask, 'rendimiento_kg_ha']
    return df_archivos

# Lista con rutas a CSVs de rendimiento
archivos_rendimientos = [
    '/home/cris/Documents/TESIS/BR_DATA/rendimientos/arroz_rs_2020.csv',
    '/home/cris/Documents/TESIS/BR_DATA/rendimientos/arroz_rs_2023.csv',
    '/home/cris/Documents/TESIS/BR_DATA/rendimientos/arroz_rs_2024.csv',
]

# Iterar y actualizar label para cada CSV de rendimiento
for archivo_rend in archivos_rendimientos:
    df_archivos = actualizar_label_con_rendimiento(df_archivos, archivo_rend)

# Eliminar columna temporal antes de guardar
df_archivos = df_archivos.drop(columns=['codigo_municipio'])

# Guardar resultado final
df_archivos.to_csv(merge_out, index=False)
