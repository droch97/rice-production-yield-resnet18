import torch
import rasterio
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from torch.utils.data import Dataset

def open_with_rasterio(file_path):
    with rasterio.open(file_path) as image:
        array = image.read()
    return array

def show_sentinel2_image_with_label_e2(sentinel2_image, label, tuple_figsize=(20, 12), num_fontsize=24):
    rgb_image = sentinel2_image[[0, 1, 2], :, :]
    rgb_image = torch.clamp((rgb_image - 0) / (0.3 - 0), 0, 1)
    rgb_image = rgb_image.permute(1, 2, 0).cpu().numpy()
    fig, axes = plt.subplots(1,2, figsize=tuple_figsize)
    axes[0].imshow(rgb_image)
    axes[0].axis('off')
    axes[0].set_title("Imagen RGB Etapa 2")
    axes[1].text(0.5, 0.5, str(label), fontsize=num_fontsize, ha='center', va='center')
    axes[1].axis('off')
    axes[1].set_title("Etiqueta")
    plt.tight_layout()
    plt.show()
    
def show_sentinel2_image_with_label_e3(sentinel2_image, label, tuple_figsize=(20, 12), num_fontsize=24):
    rgb_image = sentinel2_image[[5, 6, 7], :, :]
    rgb_image = torch.clamp((rgb_image - 0) / (0.3 - 0), 0, 1)
    rgb_image = rgb_image.permute(1, 2, 0).cpu().numpy()
    fig, axes = plt.subplots(1,2, figsize=tuple_figsize)
    axes[0].imshow(rgb_image)
    axes[0].axis('off')
    axes[0].set_title("Imagen RGB Etapa 3")
    axes[1].text(0.5, 0.5, str(label), fontsize=num_fontsize, ha='center', va='center')
    axes[1].axis('off')
    axes[1].set_title("Etiqueta")
    plt.tight_layout()
    plt.show()

def show_sentinel2_image_both_seasons(sentinel2_image, label, tuple_figsize=(20, 12), num_fontsize=24):
    rgb_image_e2 = sentinel2_image[[0, 1, 2], :, :]
    rgb_image_e2 = torch.clamp((rgb_image_e2 - 0) / (0.3 - 0), 0, 1)
    rgb_image_e2 = rgb_image_e2.permute(1, 2, 0).cpu().numpy()
    rgb_image_e3 = sentinel2_image[[5, 6, 7], :, :]
    rgb_image_e3 = torch.clamp((rgb_image_e3 - 0) / (0.3 - 0), 0, 1)
    rgb_image_e3 = rgb_image_e3.permute(1, 2, 0).cpu().numpy()
    fig, axes = plt.subplots(1, 3, figsize=tuple_figsize)
    axes[0].imshow(rgb_image_e2)
    axes[0].axis('off')
    axes[0].set_title("Imagen RGB Etapa 2")
    axes[1].imshow(rgb_image_e3)
    axes[1].axis('off')
    axes[1].set_title("Imagen RGB Etapa 3")
    axes[2].text(0.5, 0.5, str(label), fontsize=num_fontsize, ha='center', va='center')
    axes[2].axis('off')
    axes[2].set_title("Etiqueta")
    plt.tight_layout()
    plt.show()

class Sentinel2ConcatSeasonsRegressionDataset(Dataset):
    def __init__(self, folder_path, csv):
        self.csv = csv
        self.folder_path = folder_path
        df = pd.read_csv(csv)
        filenames = list(df['filename'])
        labels = list(df['label'])
        data = []
        for i in range(len(filenames)):
            filename_with_folder = folder_path + '/' + filenames[i]
            image = open_with_rasterio(filename_with_folder)
            tensor = torch.tensor(image, dtype=torch.float32)
            data.append(tensor)
            print(i, ";", labels[i])
        if len(data) != len(labels):
            raise Exception("Data list length is not equal to label list length")
        self.labels = labels
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
    
    def show_image_e2(self, idx):
        show_sentinel2_image_with_label_e2(self.data[idx], self.labels[idx])
    
    def show_image_e3(self, idx):
        show_sentinel2_image_with_label_e3(self.data[idx], self.labels[idx])

    def show_image_full(self, idx):
        show_sentinel2_image_both_seasons(self.data[idx], self.labels[idx])