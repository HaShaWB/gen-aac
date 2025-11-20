# tests/test_token_editing.py

from genaac import token_imaging, edit_token
from genaac.models import Token, EditingHistory
from genaac.utils import decode_image_from_bytes


token = Token(keyword="밥")

print("1. 밥")
pair = token_imaging(token)
history = EditingHistory(initial_pair=pair)
decode_image_from_bytes(history.get_final_pair().image).show()

print("2. 쌀밥 -> 빵")
feedback1 = "쌀밥 대신 빵을 그려주세요"
turn1 = edit_token(history, feedback1)
history.add_turn(turn1)
decode_image_from_bytes(history.get_final_pair().image).show()

print("3. 빵 -> 빵 + 딸기 잼")
feedback2 = "빵 위에 딸기 잼을 올려주세요"
turn2 = edit_token(history, feedback2)
history.add_turn(turn2)
decode_image_from_bytes(history.get_final_pair().image).show()
