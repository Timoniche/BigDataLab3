import os
import pathlib
import sys

src_module_path = os.path.join(os.getcwd(), "src")
sys.path.insert(1, src_module_path)

from database import Database  # noqa: E402
from service import Service  # noqa: E402
from utils.common_utils import generate_time_id  # noqa: E402
from logger import Logger  # noqa: E402
from server import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


class FunctionalApiTest:

    def __init__(
            self,
            client: TestClient,
    ) -> None:
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)
        self.client = client

    def test_upload_photo(self):
        images_dir = str(pathlib.Path(__file__).resolve().parent.parent.parent)
        print(images_dir)
        img_path = images_dir + '/client_images/' + '000002.jpg'

        files = {
            'file': open(img_path, 'rb')
        }
        response = self.client.post(
            url='http://localhost:8000/upload/',
            files=files,
        )

        json = response.content.decode()

        assert response.status_code == 200
        self.log.info(f'Response json: {json}')
        ground_truth = '{"filename":"000002.jpg","is_male":"female"}'

        assert json == ground_truth, f'Expected {ground_truth}, got {json}'

        self.log.info('Server Test Passed')

    def test_db_upload_photo(self):
        db = Database()
        service = Service(db)

        filename = generate_time_id()
        self.log.info(f'filename: {filename}')

        service.save_image_prediction(
            image_name=filename,
            is_male=True,
        )

        is_male_from_db = service.get_image_male(
            image_name=filename,
        )[0][0]

        assert is_male_from_db == True, f'Expected {True}, got {is_male_from_db}'

        self.log.info('Db Test Passed')


if __name__ == '__main__':
    mock_client = TestClient(app)
    api_test = FunctionalApiTest(mock_client)

    api_test.test_upload_photo()
    api_test.test_db_upload_photo()
