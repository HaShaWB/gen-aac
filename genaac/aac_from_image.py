# genaac/aac_from_image.py

from typing import List

from genaac.config import AAC_FROM_IMAGE_PROMPT, ROOT_DIR
from genaac.utils import (
    generate_banana_response,
    generate_banana_response_parallel,
    ImageTextPair,
    file_to_bytes,
)

HUMAN_SYMBOL = ImageTextPair(
    image=file_to_bytes(ROOT_DIR / "templates" / "human.png"),
    text="예시: '사람' \n주어진 이미지는 사람을 나타내는 AAC Symbol이야. 키워드에 사람이 들어간다면 참고해."
)

def aac_from_image(keyword: str, image: bytes) -> ImageTextPair:

    pair = ImageTextPair(
        image=image,
        text=f"키워드: {keyword}\n\n이미지를 그대로 스타일만 변화시키는 것이 아니라, 이미지의 객체를 AAC Symbol로 표현해야해."
    )

    messages = [
        {"role": "system", "content": AAC_FROM_IMAGE_PROMPT},
        HUMAN_SYMBOL.to_chat(),
        pair.to_chat(),
    ]

    response = generate_banana_response(messages)
    response.text = keyword

    print(f"[AAC FROM IMAGE] Generated: {keyword}")

    return response


def aac_from_image_parallel(
    keywords: List[str], 
    images: List[bytes],
    max_workers: int = 5
) -> List[ImageTextPair]:
    """
    여러 이미지를 병렬 처리하여 AAC Symbol 생성
    
    Args:
        keywords: 키워드 리스트
        images: 이미지 바이트 리스트
        max_workers: 최대 동시 실행 스레드 수
    
    Returns:
        ImageTextPair 리스트 (순서 유지)
    """

    messages_list = [
        [
            {"role": "system", "content": AAC_FROM_IMAGE_PROMPT},
            HUMAN_SYMBOL.to_chat(),
            ImageTextPair(
                image=image,
                text=f"키워드: {keyword}\n\n이미지를 그대로 스타일만 변화시키는 것이 아니라, 이미지의 객체를 AAC Symbol로 표현해야해."
            ).to_chat()
        ]
        for keyword, image in zip(keywords, images)
    ]

    pairs = generate_banana_response_parallel(messages_list, max_workers=max_workers)
    for pair, keyword in zip(pairs, keywords):
        pair.text = keyword

    print(f"[AAC FROM IMAGE PARALLEL] Generated: {keywords}")
    return pairs    