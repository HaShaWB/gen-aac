# genaac/utils/gcp_data_client.py

import os
import json
import datetime
import uuid
from pathlib import Path
from typing import Optional

import yaml
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import firestore


ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG = yaml.safe_load((ROOT_DIR / "config.yaml").read_text(encoding="utf-8"))


creditial = service_account.Credentials.from_service_account_info(
    json.loads(os.getenv("GOOGLE_CREDITIALS")),
)
storage_client = storage.Client(
    credentials=creditial, 
    project=CONFIG["database"]["project_id"]
)
bucket_client = storage_client.bucket(CONFIG["database"]["aac_image_bucket_name"])
firestore_client = firestore.Client(
    credentials=creditial, 
    project=CONFIG["database"]["project_id"],
    database=CONFIG["database"]["aac_log_database_id"],
)


def make_id(prefix: Optional[str] = None) -> str:
    kst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(kst)
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    random_uuid = str(uuid.uuid4())[:8]
    document_id = f"{timestamp}_{random_uuid}"
    if prefix:
        document_id = f"{prefix}_{document_id}"
    return document_id


def upload_file(file: bytes, blob_name: str) -> Optional[str]:
    try:
        blob = bucket_client.blob(blob_name)
        blob.upload_from_string(file)
        return blob.public_url
    except Exception as e:
        print(f"[DATA] Error uploading file to bucket: {e}")
        return None


def download_file(blob_name: str) -> Optional[bytes]:
    try:
        blob = bucket_client.blob(blob_name)
        return blob.download_as_bytes()
    except Exception as e:
        print(f"[DATA] Error downloading file from bucket: {e}")
        return None


def upload_document(collection_name: str, document: dict, document_id: str) -> Optional[str]:
    try:
        collection = firestore_client.collection(collection_name)
        collection.document(document_id).set(document)
        return document_id
    except Exception as e:
        print(f"[DATA] Error uploading document to collection: {e}")
        return None


def download_document(collection_name: str, document_id: str) -> Optional[dict]:
    try:
        collection = firestore_client.collection(collection_name)
        doc = collection.document(document_id).get()
        return doc.to_dict()
    except Exception as e:
        print(f"[DATA] Error downloading document from collection: {e}")
        return None
