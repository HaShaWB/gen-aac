# Utils 사용 가이드

`genaac/utils` 폴더에 있는 주요 유틸리티 함수들의 사용법을 정리한 문서입니다.
복잡한 설명보다는 **어떻게 쓰는지** 위주로 간단하게 작성했습니다.

---

## 1. LLM Client (`llm_client.py`)

LLM(Gemini, GPT 등)과 대화할 때 사용합니다. `litellm`을 사용하여 여러 모델을 쉽게 전환할 수 있습니다.

### 기본 텍스트 생성

가장 기본적인 대화 함수입니다. Primary 모델이 실패하면 자동으로 Secondary 모델을 시도합니다.

```python
from genaac.utils.llm_client import generate_llm_response

messages = [{"role": "user", "content": "안녕, 자기소개 좀 해줘."}]
response = generate_llm_response(messages)
print(response) # "안녕하세요! 저는..."
```

### JSON 데이터 생성

Pydantic 모델을 정의해서 정해진 포맷의 데이터를 받을 때 사용합니다.

```python
from pydantic import BaseModel
from genaac.utils.llm_client import generate_llm_response_in_json

class MovieReview(BaseModel):
    title: str
    rating: int

messages = [{"role": "user", "content": "기생충 영화 리뷰 데이터를 만들어줘."}]
review = generate_llm_response_in_json(messages, MovieReview)

print(review.title)  # "기생충"
print(review.rating) # 5
```

---

## 2. GCP Data Client (`gcp_data_client.py`)

Google Cloud Platform의 Storage(파일 저장)와 Firestore(DB)를 다룹니다.

### ID 생성

현재 시간과 랜덤 값을 조합해 유니크한 ID를 만듭니다.

```python
from genaac.utils.gcp_data_client import make_id

doc_id = make_id(prefix="user")
print(doc_id) # "user_2024-05-20_10-30-00_a1b2c3d4"
```

### 파일 업로드/다운로드 (Storage)

이미지나 파일을 클라우드 버킷에 올리고 내립니다.

```python
from genaac.utils.gcp_data_client import upload_file, download_file

# 업로드 (파일 bytes, 저장할 경로)
url = upload_file(image_bytes, "images/my_photo.png")

# 다운로드
file_bytes = download_file("images/my_photo.png")
```

### 데이터 저장/조회 (Firestore)

JSON 형태의 데이터를 DB에 저장하고 불러옵니다.

```python
from genaac.utils.gcp_data_client import upload_document, download_document

data = {"name": "Kim", "age": 30}

# 저장 (컬렉션 이름, 데이터, 문서 ID)
upload_document("users", data, "user_001")

# 조회
user_data = download_document("users", "user_001")
```

---

## 3. Imagen Client (`imagen_client.py`)

Google의 이미지 생성 모델(Imagen)을 사용합니다.

### 이미지 생성

텍스트 프롬프트를 주면 이미지를 생성해서 bytes 형태로 돌려줍니다.

```python
from genaac.utils.imagen_client import generate_imagen_response

prompt = "A futuristic city with flying cars, cyberpunk style"
image_bytes = generate_imagen_response(prompt)

# 파일로 저장 예시
with open("city.png", "wb") as f:
    f.write(image_bytes)
```

---

## 4. Image Utils (`image.py`)

이미지 처리를 위한 헬퍼 함수들입니다. 주로 PIL Image와 bytes/base64 간의 변환을 담당합니다.

### 이미지 변환

```python
from PIL import Image
from genaac.utils.image import encode_image, decode_image_from_bytes

# PIL Image -> Bytes (PNG 포맷)
img = Image.open("test.jpg")
img_bytes = encode_image(img)

# Bytes -> PIL Image
new_img = decode_image_from_bytes(img_bytes)
new_img.show()
```

### Base64 문자열 변환

Bytes를 Base64 문자열로 변환하거나, Base64 문자열을 이미지로 복원할 때 사용합니다.

```python
from genaac.utils.image import bytes_to_str, decode_image_from_str

# Bytes -> Base64 String
b64_str = bytes_to_str(img_bytes)

# Base64 String -> PIL Image
restored_img = decode_image_from_str(b64_str)
```

### Data URL 생성

이미지를 웹에서 바로 표시할 수 있는 Data URL 형식으로 변환합니다.

```python
from genaac.utils.image import png_to_url

# PNG Bytes -> Data URL
data_url = png_to_url(img_bytes)
print(data_url) # "data:image/png;base64,iVBORw0KG..."
```
