# tests/test_aac_from_keyword.py

from genaac import aac_from_keyword

response = aac_from_keyword("학교")

print(response.text)
response.show()
