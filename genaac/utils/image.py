# genaac/utils/image.py

import base64
from io import BytesIO

from PIL import Image


def image_to_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def file_to_bytes(file: str) -> bytes:
    with open(file, "rb") as f:
        return f.read()


def bytes_to_str(bytes: bytes) -> str:
    return base64.b64encode(bytes).decode('utf-8')


def bytes_to_image(bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(bytes))


def bytes_to_url(bytes: bytes, image_format: str = 'png') -> str:
    return f"data:image/{image_format};base64,{bytes_to_str(bytes)}"


def url_to_bytes(url: str) -> bytes:
    return base64.b64decode(url.split(",")[1])
    

def url_to_image(url: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(url.split(",")[1])))
