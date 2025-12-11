# tests/test_aac_syntax.py

from genaac.aac_syntax import add_cross, add_question_mark
from genaac.aac_collage import GOING_PAIR
from genaac.utils import bytes_to_image


bytes_to_image(add_cross(GOING_PAIR.image)).show()
bytes_to_image(add_question_mark(GOING_PAIR.image)).show()
