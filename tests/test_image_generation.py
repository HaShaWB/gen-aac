# tests/test_image_generation.py

from genaac import symbol_generation
from genaac.utils import bytes_to_image

keyword = "학교"
print(keyword)

result = symbol_generation(keyword)
print(result.text)
bytes_to_image(result.image).show()
