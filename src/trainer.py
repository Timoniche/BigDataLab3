import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

from img_with_name_dataloader import prepare_celeba_dataloader_with_names
from utils.common_utils import parent_dir

BATCH_SIZE = 128


def male_condition_extractor():
    attr_path = parent_dir() + '/celeba_dataset/list_attr_celeba.csv'
    df = pd.read_csv(attr_path)

    img_to_ismale = {}
    female = 0
    male = 1

    image_ids = list(df['image_id'])[:-1]
    males = list(df['Male'])[:-1]
    males = list(map(lambda x: male if x == male else female, males))

    for i in range(len(image_ids)):
        img_to_ismale[image_ids[i]] = males[i]

    return img_to_ismale


def train(
        dataloader,
        n_samples,
        classifier_save_path,
):
    rf_classifier = RandomForestClassifier(
        n_estimators=100,
        criterion='gini',
    )

    num_epochs = 1
    for epoch in range(num_epochs):
        for i, (real_images, img_names, hog_embs, is_male) in tqdm(
                enumerate(dataloader),
                total=n_samples // BATCH_SIZE
        ):
            rf_classifier.fit(hog_embs, is_male)

    with open(classifier_save_path, 'wb') as f:
        pickle.dump(rf_classifier, f)

    return rf_classifier


def main():
    img_to_male = male_condition_extractor()
    dataloader, n_samples = prepare_celeba_dataloader_with_names(
        img_to_male=img_to_male,
        batch_size=BATCH_SIZE,
    )
    train(
        dataloader,
        n_samples,
        classifier_save_path='./../experiments/random_forest_pretrained.pkl'
    )


if __name__ == '__main__':
    main()
