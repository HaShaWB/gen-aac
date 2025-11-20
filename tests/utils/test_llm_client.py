# tests/utils/test_llm_client

from pydantic import BaseModel

from genaac.utils import generate_llm_response, generate_llm_response_in_json


test_messages = [
    {"role": "system", "content": "You are a helpful assistant. Answer in one sentence."},
    {"role": "user", "content": "Hello there! How are you?"}
]

class Answer(BaseModel):
    positive_response: str
    negative_response: str
    

# 1. generate_llm_response
print("1. generate_llm_response")
response = generate_llm_response(test_messages)
print(f"Response: {response}")
print()


# 2. generate_llm_response_in_json
print("2. generate_llm_response_in_json")
response: Answer = generate_llm_response_in_json(test_messages, Answer)
print(f"Response: {response.model_dump_json()}")
print()
