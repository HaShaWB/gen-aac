# genaac/aac_syntax.py

from pathlib import Path

from PIL import Image

from genaac.utils.image import bytes_to_image, image_to_bytes
from genaac.config import ROOT_DIR

# 템플릿 이미지 경로
_TEMPLATES_DIR = ROOT_DIR / "templates"
_CROSS_TEMPLATE = _TEMPLATES_DIR / "cross.png"
_QUESTION_MARK_TEMPLATE = _TEMPLATES_DIR / "question_mark.png"


def add_cross(image: bytes) -> bytes:
    """
    1K x 1K (1024x1024) 이미지에 검은 테두리의 빨간 X를 추가
    """
    img = bytes_to_image(image).convert("RGBA")
    
    # 이미지 크기가 1024x1024가 아니면 리사이즈
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    # X 템플릿 이미지 로드
    cross_img = Image.open(_CROSS_TEMPLATE)
    
    # 원본 이미지 위에 X 이미지를 합성
    img.paste(cross_img, (0, 0), cross_img)
    
    # RGB로 변환 후 반환
    result = img.convert("RGB")
    return image_to_bytes(result)


def add_question_mark(image: bytes) -> bytes:
    """
    1K x 1K (1024x1024) 이미지에 반투명한 빨간 물음표를 추가
    """
    img = bytes_to_image(image).convert("RGBA")
    
    # 이미지 크기가 1024x1024가 아니면 리사이즈
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    # 물음표 템플릿 이미지 로드
    question_mark_img = Image.open(_QUESTION_MARK_TEMPLATE)
    
    # 원본 이미지 위에 물음표 이미지를 합성
    img.paste(question_mark_img, (0, 0), question_mark_img)
    
    # RGB로 변환 후 반환
    result = img.convert("RGB")
    return image_to_bytes(result)
