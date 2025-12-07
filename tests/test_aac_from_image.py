# tests/test_aac_from_image.py

from genaac import aac_from_image
from genaac.config import ROOT_DIR
from genaac.utils import file_to_bytes

image = file_to_bytes(ROOT_DIR / "tests" / "성당.png")

response = aac_from_image("성당", image)

print(response.text)
response.show()
