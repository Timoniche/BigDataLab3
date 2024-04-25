import requests

from utils.common_utils import parent_dir


def main():
    img_path = parent_dir() + '/client_images/' + '000003.jpg'

    files = {
        'file': open(img_path, 'rb')
    }
    response = requests.post(
        url='http://localhost:8000/upload/',
        files=files,
    )

    print(response)
    print(response.content)


if __name__ == '__main__':
    main()
