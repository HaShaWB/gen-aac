# tests/test_token_imaging.py

from genaac import token_imaging, token_imaging_batch
from genaac.models import Token
from genaac.utils import decode_image_from_bytes


print("1. 단일 Imaging")
token = Token(keyword="밥")

pair = token_imaging(token)

image = decode_image_from_bytes(pair.image)
image.show()


print("2. 병렬 Imaging")
token2 = Token(keyword="빵")

pairs = token_imaging_batch([token, token2])

for pair in pairs:
    image = decode_image_from_bytes(pair.image)
    image.show()
