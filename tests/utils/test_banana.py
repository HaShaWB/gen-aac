# tests/utils/test_banana.py

from genaac.utils import generate_banana_response, bytes_to_image


test_messages = [
    {"role": "user", "content": "하늘색 줄무늬를 가진 흰 고양이를 그려줘"}
]

response = generate_banana_response(test_messages)

print(response.text)
bytes_to_image(response.image).show()
