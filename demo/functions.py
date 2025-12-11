# demo/functions.py

from genaac import (
    aac_from_keyword, aac_from_keyword_parallel,
    aac_from_image,
    tokenizing, Token,
    add_cross, add_question_mark
)
from demo.user_data import UserData
from genaac.utils import ImageTextPair


def _process_token(token: Token, user_data: UserData):
    print(f"[PROCESS TOKEN] Processing: {token.keyword}")
    if token.keyword in user_data.symbol_gallery:
        pair = user_data.symbol_gallery[token.keyword]
        pair = ImageTextPair(image=pair.image, text=token.keyword)
    else:
        pair = aac_from_keyword(token.keyword)
        user_data.add_symbol(pair)

    if token.syntax == "부정":
        pair.image = add_cross(pair.image)
        pair.text = f"(부정) {token.keyword}"
    
    elif token.syntax == "의문":
        pair.image = add_question_mark(pair.image)
        pair.text = f"(의문) {token.keyword}"
    
    return pair


def process_sentence(sentence: str, user_data: UserData):
    print(f"[PROCESS SENTENCE] Processing: {sentence}")
    tokens = tokenizing(sentence)

    tokens_without_order = list(set([token.keyword for token in tokens if token.keyword not in user_data.symbol_gallery]))
    pairs_without_order = aac_from_keyword_parallel(tokens_without_order)
    for pair in pairs_without_order:
        user_data.add_symbol(pair)
    
    return [
        _process_token(token, user_data) for token in tokens
    ]


def process_keyword(keyword: str, user_data: UserData):
    pair = aac_from_keyword(keyword)
    user_data.add_symbol(pair)
    return pair


def process_image_keyword(keyword: str, image: bytes, user_data: UserData):
    pair = aac_from_image(keyword, image)
    user_data.add_symbol(pair)
    return pair