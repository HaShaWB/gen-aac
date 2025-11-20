# tests/test_token_imaging.py

from genaac import token_imaging
from genaac.models import Token
from genaac.utils import decode_image_from_bytes


token = Token(keyword="밥")

pair = token_imaging(token)

image = decode_image_from_bytes(pair.image)
image.show()
