import pathlib

import requests


# noinspection PyMethodMayBeStatic
class FunctionalApiTest:

    def __init__(
            self,
    ) -> None:
        pass

    def test_upload_photo(self):
        images_dir = str(pathlib.Path().resolve().parent.parent)
        img_path = images_dir + '/client_images/' + '000003.jpg'

        files = {
            'file': open(img_path, 'rb')
        }
        response = requests.post(
            url='http://localhost:8000/upload/',
            files=files,
        )

        print(response)
        json = response.content.decode()
        print(json)

        assert response.status_code == 200
        ground_truth = '{"filename":"000003.jpg","is_male":"male"}'

        assert json == ground_truth, f'Expected {ground_truth}, got {json}'

        print('Test passed')


if __name__ == '__main__':
    api_test = FunctionalApiTest()
    api_test.test_upload_photo()
