# tests/test_tokenize.py

from genaac import tokenize as genaac_tokenize


sentence = "오늘 학교에서 밥 먹고 왔어?"
response = genaac_tokenize(sentence)

print(f"Sentence: {sentence}")
for token in response.tokens:
    print(token)
