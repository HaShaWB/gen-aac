# tests/test_tokenizing.py

from genaac.tokenizing import tokenizing

def test_tokenizing():
    sentence = "집에 갈까?"
    tokens = tokenizing(sentence)
    print(tokens)

if __name__ == "__main__":
    test_tokenizing()
