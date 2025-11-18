# tests/utils/gcp_data_client.py

from PIL import Image

from genaac.utils import (
    make_id,
    upload_file,
    download_file,
    upload_document,
    download_document,
    encode_image,
    decode_image_from_bytes,
)


# 1. make_id
print("1. make_id")
print(f"random_id: {make_id()}")
print(f"random_id with prefix: {make_id(prefix='test')}")
print()


# 2. upload_file
print("2. upload_file")
image = Image.open("tests/utils/test_image.png")
image_bytes = encode_image(image)
url = upload_file(image_bytes, "test_image.png")
print(f"url: {url}")
print()


# 3. download_file
print("3. download_file")
image_bytes = download_file("test_image.png")
image = decode_image_from_bytes(image_bytes)
image.show()
print()


# 4. upload_document
print("4. upload_document")
document = {
    "name": "test_document",
    "description": "test_description",
}
document_id = upload_document("test_collection", document, "test_log")
print(f"document_id: {document_id}")
print()


# 5. download_document
print("5. download_document")
document = download_document("test_collection", "test_log")
print(f"document: {document}")
print()
