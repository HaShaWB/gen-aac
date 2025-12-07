# genaac/utils/image.py

import base64 as b64
import re
from io import BytesIO

import httpx
from PIL import Image


def bytes_to_image(image_bytes: bytes) -> Image.Image:
    """bytes 데이터를 PIL Image 객체로 변환"""
    return Image.open(BytesIO(image_bytes))


def bytes_to_base64(image_bytes: bytes) -> str:
    """bytes 데이터를 base64 문자열로 인코딩"""
    return b64.b64encode(image_bytes).decode("utf-8")


def bytes_to_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """bytes 데이터를 data URL 형식으로 변환"""
    encoded = bytes_to_base64(image_bytes)
    return f"data:{mime_type};base64,{encoded}"



def file_to_bytes(file_path: str) -> bytes:
    """파일을 bytes 데이터로 변환"""
    with open(file_path, "rb") as file:
        return file.read()


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    """PIL Image 객체를 bytes 데이터로 변환"""
    buffer = BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()


def base64_to_bytes(base64_str: str) -> bytes:
    """base64 문자열을 bytes 데이터로 디코딩"""
    return b64.b64decode(base64_str)


def url_to_bytes(url: str) -> bytes:
    """URL에서 이미지 bytes 데이터 추출
    
    data URL 또는 HTTP(S) URL 모두 지원
    """
    # data URL 처리
    if url.startswith("data:"):
        match = re.match(r"data:[^;]+;base64,(.+)", url)
        if match:
            return base64_to_bytes(match.group(1))
        raise ValueError("Invalid data URL format")
    
    # HTTP(S) URL 처리
    response = httpx.get(url)
    response.raise_for_status()
    return response.content
