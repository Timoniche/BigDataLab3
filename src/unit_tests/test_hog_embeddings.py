import os
import pathlib
import sys
import unittest

import numpy as np

sys.path.insert(1, os.path.join(os.getcwd(), "src"))

from logger import Logger  # noqa: E402

from images_dataset import hog_embedding  # noqa: E402


class TestHogEmbeddings(unittest.TestCase):

    def setUp(self) -> None:
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)

        images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
        self.log.info(f'images dir {images_dir}')
        self.img_path = images_dir + '/client_images/' + '000001.jpg'

    def test_hog_embeddings(self):
        hog_embs = hog_embedding(self.img_path)

        cur_dir = str(pathlib.Path(__file__).resolve().parent)
        with open(f'{cur_dir}/ground_truth/hog_embeddings.txt', 'r') as f:
            embs = f.readline()
            ground_truth = list(map(float, embs.split()))

        np.testing.assert_almost_equal(ground_truth, hog_embs, decimal=5)

        self.log.info('Hog Embeddings Test Passed')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
