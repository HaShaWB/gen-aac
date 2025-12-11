# tests/test_aac_collage.py

from genaac import aac_collage
from genaac import aac_from_keyword


sub_keyword = aac_from_keyword("학교(school)")
response = aac_collage("go", sub_keyword)


sub_keyword.show()
print(response.text)
response.show()