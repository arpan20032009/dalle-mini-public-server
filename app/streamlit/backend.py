# Client requests to Dalle-Mini Backend server

import base64
from io import BytesIO

import requests
from PIL import Image


class ServiceError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


def get_images_from_backend(prompt, backend_url):
    r = requests.post(backend_url, json={"prompt": prompt})
    if r.status_code != 200:
        raise ServiceError(r.status_code)
    json = r.json()
    images = json["images"]
    images = [Image.open(BytesIO(base64.b64decode(img))) for img in images]
    version = json.get("version", "unknown")
    return {"images": images, "version": version}


def get_model_version(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["version"]
    else:
        raise ServiceError(r.status_code)
