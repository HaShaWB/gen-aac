# genaac/utils/image.py

import base64
from io import BytesIO

from PIL import Image


def encode_image(image: Image.Image) -> bytes:
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    return img_bytes


def encode_image_to_str(image: Image.Image) -> str:
    img_bytes = encode_image(image)
    return base64.b64encode(img_bytes).decode('utf-8')
    

def decode_image_from_bytes(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes))


def decode_image_from_str(image_str: str) -> Image.Image:
    return decode_image_from_bytes(base64.b64decode(image_str))
    