import torch.utils.data as td

from torchvision import transforms

from images_dataset import ImagesDataset, IMAGE_SIZE
from utils.common_utils import parent_dir

transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])


def prepare_celeba_dataloader_with_names(img_to_male, batch_size):
    imgs_path = parent_dir() + '/celeba_dataset/data/img_align_celeba'
    dataset = ImagesDataset(
        imgs_dir=imgs_path,
        img_to_male=img_to_male,
        transform=transform
    )
    n_samples = dataset.n_samples
    dataloader = td.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=3,
        pin_memory=True
    )
    return dataloader, n_samples
