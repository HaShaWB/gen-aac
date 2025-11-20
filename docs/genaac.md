# Genaac Core 사용 가이드

`genaac` 패키지의 핵심 로직인 토큰화(Tokenize), 이미지 생성(Imaging), 편집(Editing) 기능을 담당하는 모듈들에 대한 문서입니다.
각 단계별로 사용자의 입력을 처리하고 결과물을 생성하는 방법을 설명합니다.

---

## 1. Tokenize (`tokenize.py`)

사용자가 입력한 문장을 분석하여 구조화된 토큰 데이터로 변환합니다.

### 문장 토큰화

입력된 문장을 LLM을 통해 분석하여 `TokenizingResponse` 객체로 반환합니다.

```python
from genaac.tokenize import tokenize

sentence = "빨간 모자를 쓴 고양이가 춤을 추고 있다."
response = tokenize(sentence)

# response는 TokenizingResponse 객체입니다.
# 내부 구조는 models.py에 정의된 TokenizingResponse를 따릅니다.
print(response) 
```

---

## 2. Token Imaging (`token_imaging.py`)

추출된 토큰을 바탕으로 이미지 생성 프롬프트를 만들고, 실제 이미지를 생성합니다.

### 토큰 -> 프롬프트 변환 (`token_to_prompt`)

토큰 정보를 바탕으로 LLM을 사용하여 이미지 생성용 프롬프트를 작성합니다. `few_shots`를 제공하여 스타일을 유도할 수 있습니다.

```python
from genaac.token_imaging import token_to_prompt
from genaac.models import Token

# 예시 토큰 (실제로는 tokenize 결과에서 얻음)
my_token = Token(...) 

prompt = token_to_prompt(my_token)
print(prompt) # "A cat wearing a red hat dancing..."
```

### 토큰 -> 이미지 생성 (`token_imaging`)

프롬프트 생성부터 이미지 생성까지 한 번에 처리합니다. 결과는 `TokenPromptImagePair`로 반환됩니다.

```python
from genaac.token_imaging import token_imaging

# 이미지 생성 (프롬프트 생성 -> 이미지 생성)
result_pair = token_imaging(my_token)

print(result_pair.prompt) # 생성된 프롬프트
# result_pair.image는 생성된 이미지 데이터(bytes)입니다.
```

---

## 3. Token Editing (`token_editing.py`)

생성된 이미지에 대해 사용자의 피드백을 반영하여 수정합니다. 대화 히스토리를 기반으로 새로운 프롬프트와 이미지를 생성합니다.

### 토큰 수정 (`edit_token`)

이전 대화 기록(`EditingHistory`)과 사용자의 추가 요구사항(`user_feedback`)을 받아 새로운 수정 턴(`EditingTurn`)을 생성합니다.

```python
from genaac.token_editing import edit_token
from genaac.models import EditingHistory

# 이전 히스토리 객체 (초기 생성 결과 포함)
history = EditingHistory(...) 
user_feedback = "모자를 파란색으로 바꿔줘"

# 수정 요청 처리
new_turn = edit_token(history, user_feedback)

print(new_turn.response.prompt) # 수정된 프롬프트
# new_turn.result.image에 수정된 이미지가 담깁니다.
```
