import requests
from io import BytesIO
import base64
import os


def download_image(url: str):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    return image_data


def save_bytes_to_image(bytes_data, file_path):
    with open(file_path, 'wb') as file:
        file.write(bytes_data)


def base64_to_bytes(base64_string):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    bytes_data = base64.b64decode(base64_string)
    return bytes_data


def ensure_directory_exists(dir_path):
    """
        如果目录不存在则创建目录
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def get_base_folder():
    # utils
    dir = os.path.dirname(os.path.realpath(__file__))
    # src
    dir = os.path.dirname(dir)
    # vines-worker-python
    dir = os.path.dirname(dir)
    return dir


def get_statics_folder():
    base_dir = get_base_folder()
    return os.path.join(base_dir, "statics")


def get_and_ensure_exists_tmp_files_folder():
    base_dir = get_base_folder()
    tmp_files_folder = os.path.join(base_dir, "tmp-files")
    ensure_directory_exists(tmp_files_folder)
    return tmp_files_folder
