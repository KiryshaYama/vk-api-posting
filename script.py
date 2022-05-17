import requests
import os
import dotenv

from random import Random
from urllib.parse import urljoin, urlparse


def check_for_errors(response):
    response.raise_for_status()
    if 'error' in response.json():
        print(response.json()['error'])
        raise requests.HTTPError


def get_random_comics_info():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_comic_data = response.json()
    comic_count = last_comic_data['num']
    index = Random().randint(1, comic_count)
    url = f'https://xkcd.com/{index}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    return comic_data['alt'], comic_data['img']


def download_img(img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    with open('xkcd.png', 'wb') as file:
        file.write(response.content)


def get_upload_url(group_id, access_token, api_version):
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': api_version
    }
    response = requests.get(
        'https://api.vk.com/method/photos.getWallUploadServer',
        params=params
    )
    check_for_errors(response)
    return response.json()['response']['upload_url']


def upload_img(upload_url, img_name, access_token, api_version):
    with open(img_name, 'rb') as file:
        files = {
            'photo': file,
            'access_token': access_token,
            'v': api_version
        }
        response = requests.post(upload_url, files=files)
        check_for_errors(response)
        return response.json()


def save_wall_photo(photo_properties, group_id, access_token, api_version):
    params = {
        'group_id': group_id,
        'photo': photo_properties['photo'],
        'server': photo_properties['server'],

        'hash': photo_properties['hash'],
        'access_token': access_token,
        'v': api_version
    }
    response = requests.get(
        'https://api.vk.com/method/photos.saveWallPhoto',
        params=params
    )
    check_for_errors(response)
    result = response.json()['response'][0]
    return f"photo{result['owner_id']}_{result['id']}"


def publish_wall_post(saved_photo_name, alt, group_id, access_token, api_version):
    params = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': alt,
        'attachments': saved_photo_name,
        'access_token': access_token,
        'v': api_version
    }
    response = requests.get(
        'https://api.vk.com/method/wall.post',
        params=params
    )
    check_for_errors(response)
    print('Comics posted')


def main():
    dotenv.load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    group_id = int(os.getenv('GROUP_ID'))
    api_version = os.getenv('API_VERSION')
    alt, img_url = get_random_comics_info()
    download_img(img_url)
    try:
        upload_url = get_upload_url(group_id, access_token, api_version)
        img_name = 'xkcd.png'
        photo_properties = upload_img(upload_url, img_name, access_token, api_version)
        saved_photo_name = save_wall_photo(photo_properties, group_id, access_token, api_version)
        publish_wall_post(saved_photo_name, alt, group_id, access_token, api_version)
    finally:
        os.remove('xkcd.png')


if __name__ == '__main__':
    main()
