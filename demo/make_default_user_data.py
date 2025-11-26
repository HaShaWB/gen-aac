# demo/make_default_user_data.py
# Do not import this code

from concurrent.futures import ThreadPoolExecutor

from user_data import UserData
from genaac.token_imaging import generate_imagen_response
from genaac.models import EditingHistory, TokenPromptPair, Token, TokenPromptImagePair

user_data = UserData(user_id="default")

tokens = [
    Token(keyword="물음", prompt="질문하거나 무언가를 궁금해하는 상황"),
    Token(keyword="먹다", prompt="음식을 입으로 넣어 섭취하는 행위"),
    Token(keyword="좋아", prompt="어떤 것을 선호하거나 긍정적으로 생각하는 감정"),
    Token(keyword="싫어", prompt="어떤 것을 거부하거나 좋아하지 않는 감정")
]

pairs = [
    TokenPromptPair(token=tokens[0], prompt="Simple flat vector illustration on white background with no text or letters. Large question mark symbol (?) as the main element in the center, filled with Red (#FF0000). Below the question mark, upper body of a person with circular PeachPuff (#FFDAB9) face, Black (#000000) semicircle hair on top, simple dot eyes and small curved line for neutral mouth. Person wearing Blue (#0000FF) short-sleeve shirt. One hand raised to chin in thinking gesture, showing curious or wondering expression. Only shoulders and head visible, no lower body shown. All elements constructed from basic geometric shapes (circles, semicircles) with rounded corners. Thick black outline (32px) around all objects including the question mark and person. No shadows, no gradients, flat colors only, centered composition."),
    TokenPromptPair(token=tokens[1], prompt="Simple flat vector illustration on white background with no text or letters. Upper body of a person in the center with circular PeachPuff (#FFDAB9) face, Black (#000000) semicircle hair on top. Simple dot eyes and open circular mouth showing eating expression. Person wearing Blue (#0000FF) short-sleeve shirt. One hand holding a simple spoon shape in Red (#FF0000), bringing it toward the mouth. The spoon positioned between hand and mouth, clearly showing the eating gesture. Only shoulders and head visible, no lower body shown. All elements constructed from basic geometric shapes (circles, semicircles, simple rectangles for spoon) with rounded corners. Thick black outline (32px) around all objects including the person and spoon. No shadows, no gradients, flat colors only, centered composition."),
    TokenPromptPair(token=tokens[2], prompt="Simple flat vector illustration on white background with no text or letters. Upper body of a person in the center with circular PeachPuff (#FFDAB9) face, Black (#000000) semicircle hair on top. Simple dot eyes and wide upward curved line for big smiling mouth showing happy expression. Person wearing Blue (#0000FF) short-sleeve shirt. One hand raised giving thumbs up gesture with thumb pointing upward, clearly visible. Large red heart symbol (Red #FF0000) floating above the person's head on the right side. Only shoulders and head visible, no lower body shown. All elements constructed from basic geometric shapes (circles, semicircles, heart shape) with rounded corners. Thick black outline (32px) around all objects including the person, hand, and heart. No shadows, no gradients, flat colors only, centered composition."),
    TokenPromptPair(token=tokens[3], prompt="Simple flat vector illustration on white background with no text or letters. Upper body of a person in the center with circular PeachPuff (#FFDAB9) face, Black (#000000) semicircle hair on top. Simple dot eyes and downward curved line for frowning mouth showing unhappy expression. Person wearing Blue (#0000FF) short-sleeve shirt. One hand raised with palm facing outward in stop/reject gesture clearly visible. Large red X mark symbol (Red #FF0000) floating beside the person on the left side, made of two diagonal crossing lines. Only shoulders and head visible, no lower body shown. All elements constructed from basic geometric shapes (circles, semicircles, diagonal lines for X) with rounded corners. Thick black outline (32px) around all objects including the person, hand, and X mark. No shadows, no gradients, flat colors only, centered composition.")
]

t_pairs = []

# 병렬로 이미지 생성 처리
def _generate_image_pair(pair: TokenPromptPair) -> TokenPromptImagePair:
    image = generate_imagen_response(pair.prompt)
    print(f"Finish: {pair.token.keyword}")
    return TokenPromptImagePair(token=pair.token, prompt=pair.prompt, image=image)

with ThreadPoolExecutor(max_workers=4) as executor:
    t_pairs = list(executor.map(_generate_image_pair, pairs))

historys = []

for t_pair in t_pairs:
    historys.append(EditingHistory(initial_pair=t_pair))


for history in historys:
    user_data.add_history(history)

user_data.upload_to_server()

