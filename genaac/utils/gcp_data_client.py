# genaac/utils/gcp_data_client.py

import os
import json
import datetime
import concurrent.futures
from typing import Dict
import uuid
from typing import Optional

from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import firestore

from genaac.config import CONFIG


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


def upload_file(file: bytes, blob_name: str, bucket_name: Optional[str] = None) -> Optional[str]:
    try:
        if bucket_name is None:
            blob = bucket_client.blob(blob_name)
        else: 
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
        blob.upload_from_string(file)
        return blob.public_url
    except Exception as e:
        print(f"[DATA] Error uploading file to bucket: {e}")
        return None


def download_file(blob_name: str, bucket_name: Optional[str] = None) -> Optional[bytes]:
    try:
        if bucket_name is None:
            blob = bucket_client.blob(blob_name)
        else:
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
        return blob.download_as_bytes()
    except Exception as e:
        print(f"[DATA] Error downloading file from bucket: {e}")
        return None


def list_files(prefix: str, bucket_name: Optional[str] = None) -> Optional[list[str]]:
    """
    GCS 버킷 내 특정 prefix 를 가진 파일 목록을 조회함.

    Args:
        prefix (str): 조회할 파일 경로 prefix
        bucket_name (Optional[str]): 대상 Bucket 이름. None 일 경우 기본 Bucket 사용

    Returns:
        Optional[list[str]]: 파일명 리스트. 실패 시 None 반환
    """
    try:
        # 버킷 클라이언트 설정
        if bucket_name is None:
            bucket = bucket_client
        else:
            bucket = storage_client.bucket(bucket_name)

        # Blob 목록 조회
        blobs = bucket.list_blobs(prefix=prefix)

        # 이름 리스트 반환
        return [blob.name for blob in blobs]

    except Exception as e:
        print(f"[DATA] Error listing files in bucket: {e}")
        return None


def download_folder(prefix: str, bucket_name: Optional[str] = None) -> Optional[Dict[str, bytes]]:
    """
    GCS 버킷 내 특정 prefix 를 가진 폴더(파일들)를 병렬로 다운로드함.

    ThreadPoolExecutor 를 사용하여 여러 파일을 동시에 다운로드함으로써 속도를 향상시킴.

    Args:
        prefix (str): 다운로드할 폴더 경로 prefix
        bucket_name (Optional[str]): 대상 Bucket 이름. None 일 경우 기본 Bucket 사용

    Returns:
        Optional[Dict[str, bytes]]: {파일명(경로제외): 바이트 데이터} 형태의 딕셔너리. 실패 시 None 반환
    """
    try:
        # 버킷 클라이언트 설정
        if bucket_name is None:
            bucket = bucket_client
        else:
            bucket = storage_client.bucket(bucket_name)

        # Blob 목록 조회
        blobs = list(bucket.list_blobs(prefix=prefix))
        
        results = {}
        
        def _download_blob(blob):
            # blob.name 은 전체 경로를 포함하므로, os.path.basename 을 사용하여 파일명만 추출함
            return os.path.basename(blob.name), blob.download_as_bytes()

        # 병렬 다운로드 실행 (ThreadPoolExecutor 사용)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # future 객체들을 생성
            future_to_blob = {executor.submit(_download_blob, blob): blob for blob in blobs}
            
            for future in concurrent.futures.as_completed(future_to_blob):
                blob = future_to_blob[future]
                try:
                    name, content = future.result()
                    results[name] = content
                except Exception as e:
                    print(f"[DATA] Error downloading blob {blob.name}: {e}")

        return results

    except Exception as e:
        print(f"[DATA] Error downloading folder from bucket: {e}")
        return None


def upload_folder(folder_data: Dict[str, bytes], prefix: str, bucket_name: Optional[str] = None) -> Optional[list[str]]:
    """
    Dict 형태의 파일 데이터를 GCS 버킷 내 특정 prefix 폴더에 병렬로 업로드함.

    ThreadPoolExecutor 를 사용하여 여러 파일을 동시에 업로드함으로써 속도를 향상시킴.

    Args:
        folder_data (Dict[str, bytes]): {파일명: 바이트 데이터} 형태의 딕셔너리
        prefix (str): 업로드할 폴더 경로 prefix
        bucket_name (Optional[str]): 대상 Bucket 이름. None 일 경우 기본 Bucket 사용

    Returns:
        Optional[list[str]]: 업로드된 파일명 리스트. 실패 시 None 반환
    """
    try:
        # 버킷 클라이언트 설정
        if bucket_name is None:
            bucket = bucket_client
        else:
            bucket = storage_client.bucket(bucket_name)

        uploaded_files = []

        def _upload_file(filename, content):
            # prefix 와 파일명을 결합하여 blob 경로 생성
            # GCS 경로는 항상 슬래시(/)를 사용
            blob_path = f"{prefix}/{filename}"
            blob = bucket.blob(blob_path)
            blob.upload_from_string(content)
            return filename

        # 병렬 업로드 실행 (ThreadPoolExecutor 사용)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # future 객체들을 생성
            future_to_file = {
                executor.submit(_upload_file, filename, content): filename 
                for filename, content in folder_data.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                filename = future_to_file[future]
                try:
                    # 업로드 성공 시 파일명 반환
                    result_filename = future.result()
                    uploaded_files.append(result_filename)
                except Exception as e:
                    print(f"[DATA] Error uploading file {filename}: {e}")

        return uploaded_files

    except Exception as e:
        print(f"[DATA] Error uploading folder to bucket: {e}")
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
