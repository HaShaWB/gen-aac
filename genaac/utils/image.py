# genaac/utils/image.py

import base64
from io import BytesIO

from PIL import Image


def encode_image(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def bytes_to_str(bytes: bytes) -> str:
    return base64.b64encode(bytes).decode('utf-8')


def png_to_url(png_bytes: bytes) -> str:
    return f"data:image/png;base64,{bytes_to_str(png_bytes)}"
    

def decode_image_from_bytes(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes))


def decode_image_from_str(image_str: str) -> Image.Image:
    return decode_image_from_bytes(base64.b64decode(image_str))
    