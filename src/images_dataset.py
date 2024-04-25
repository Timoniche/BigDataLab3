from torch.utils.data import Dataset
from typing import Callable
from PIL import Image
from skimage.feature import hog

import os
import cv2

IMAGE_SIZE = 64


def extract_hog_features(image):
    hog_features = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=False
    )

    return hog_features


def hog_embedding(img_path):
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    hog_features = extract_hog_features(img_gray)

    return hog_features


class ImagesDataset(Dataset):
    def __init__(
            self,
            imgs_dir: str,
            img_to_male: dict,
            transform: Callable = None
    ):
        # 202599
        self.img_to_male = img_to_male
        self.imgs_paths = self.__load_imgs_paths(imgs_dir)
        self.n_samples = len(self.imgs_paths)
        self.transform = transform

    def __load_imgs_paths(self, dir_from):
        imgs_paths = [os.path.join(dir_from, filename) for filename in os.listdir(dir_from) if
                      os.path.isfile(os.path.join(dir_from, filename))]
        imgs_paths = list(filter(lambda s: s.endswith('.jpg'), imgs_paths))
        imgs_paths = list(filter(lambda s: os.path.basename(s) in self.img_to_male, imgs_paths))
        return imgs_paths

    def __len__(self):
        return len(self.imgs_paths)

    def __getitem__(self, index):
        img_path = self.imgs_paths[index]
        hog_emb = hog_embedding(img_path)

        img = Image.open(img_path).convert('RGB')

        img_name = os.path.basename(img_path)

        if self.transform:
            img = self.transform(img)

        is_male = self.img_to_male[img_name]

        return img, img_name, hog_emb, is_male
