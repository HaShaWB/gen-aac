# tests/utils/imagen_client.py

from genaac.utils import generate_imagen_response
from genaac.utils import decode_image_from_bytes

# generate_imagen_response
print("generate_imagen_response")
response = generate_imagen_response("A beautiful sunset over a calm ocean.")
img = decode_image_from_bytes(response)
img.show()
print()
