import requests
import os
import dotenv

from random import Random
from urllib.parse import urljoin, urlparse


def check_for_errors(response):
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
    img_name = os.path.basename(urlparse(img_url).path)
    img_path = os.path.join(img_name)
    with open(img_path, 'wb') as file:
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
    return response


def upload_img(response, img_name, access_token, api_version):
    with open(img_name, 'rb') as file:
        url_post = response.json()['response']['upload_url']
        files = {
            'photo': file,
            'access_token': access_token,
            'v': api_version
        }
        response = requests.post(url_post, files=files)
        check_for_errors(response)
        return response


def save_wall_photo(response, group_id, access_token, api_version):
    params = {
        'group_id': group_id,
        'photo': response.json()['photo'],
        'server': response.json()['server'],

        'hash': response.json()['hash'],
        'access_token': access_token,
        'v': api_version
    }
    response = requests.get(
        'https://api.vk.com/method/photos.saveWallPhoto',
        params=params
    )
    check_for_errors(response)
    return response


def wall_post(response, alt, group_id, access_token, api_version):
    attachments = 'photo'\
                  + str(response.json()['response'][0]['owner_id'])+'_'\
                  + str(response.json()['response'][0]['id'])
    params = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': alt,
        'attachments': attachments,
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
    response = get_upload_url(group_id, access_token, api_version)
    img_name = os.path.basename(urlparse(img_url).path)
    response = upload_img(response, img_name, access_token, api_version)
    response = save_wall_photo(response, group_id, access_token, api_version)
    wall_post(response, alt, group_id, access_token, api_version)
    os.remove(img_name)


if __name__ == '__main__':
    main()
