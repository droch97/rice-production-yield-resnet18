import os
import pandas as pd

files_path = '/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/images'
file_csv = '/home/cris/Documents/TESIS/BR_DATA/DATASETCONCAT64/file_labeled_final.csv'
files = os.listdir(files_path)

df = pd.read_csv(file_csv)

for file in files:
    if not file in df['filename'].values:
        file_path = os.path.join(files_path, file)
        os.remove(file_path)
        print(f'Removed: {file_path}')

