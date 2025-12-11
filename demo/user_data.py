# demo/user_data.py

import hashlib
from typing import Dict

import streamlit as st
from pydantic import BaseModel

from genaac.utils import ImageTextPair, download_folder, upload_folder, upload_file, make_id
from genaac.config import CONFIG
from genaac.aac_from_keyword import aac_from_keyword
from genaac.aac_from_image import aac_from_image
from genaac.convert_keyword import convert_keyword


USER_DATA_BUCKET_NAME = CONFIG["database"]["user_data_bucket_name"]


def get_user_hash() -> str:
    """
    접속한 유저를 IP + 브라우저 정보 조합으로 고유 식별한다.
    같은 기기(같은 IP, 같은 브라우저)에서는 새로고침해도 동일한 해시 반환.
    """
    # Streamlit 컨텍스트에서 클라이언트 정보 추출
    headers = st.context.headers
    
    if headers is None:
        # 헤더 정보가 없는 경우 기본 해시 생성
        return hashlib.sha256("default_user".encode()).hexdigest()[:12]
    
    # IP와 브라우저 정보를 조합하여 fingerprint 생성
    remote_ip = headers.get("X-Forwarded-For", headers.get("X-Real-Ip", "127.0.0.1"))
    user_agent = headers.get("User-Agent", "unknown_agent")
    accept_lang = headers.get("Accept-Language", "")
    
    # IP + 브라우저 정보 조합 (새로고침해도 동일)
    unique_str = f"{remote_ip}_{user_agent}_{accept_lang}"
    
    # SHA256으로 해싱하여 짧은 ID 생성
    return hashlib.sha256(unique_str.encode()).hexdigest()[:12]


class UserData(BaseModel):
    user_id: str = get_user_hash()
    symbol_gallery: Dict[str, ImageTextPair] = {}


    def add_symbol(self, pair: ImageTextPair):
        self.symbol_gallery[pair.text] = pair
        self.upload_symbol(pair.text)

    
    def upload_symbol(self, keyword):
        pair = self.symbol_gallery[keyword]
        data = {f"{keyword}.png": pair.image}
        prefix = f"{self.user_id}/symbol_gallery"
        upload_folder(data, prefix, USER_DATA_BUCKET_NAME)
        
        print(f"[USER DATA] Upload {self.user_id}: {keyword}")


    def upload_userdata(self):
        """
        로컬의 심볼 갤러리 이미지들을 서버(GCS)로 병렬 업로드함.
        """
        # 업로드할 데이터 준비 {파일명: 데이터}
        upload_data = {}
        for keyword, pair in self.symbol_gallery.items():
            if pair.image:
                upload_data[f"{keyword}.png"] = pair.image
        
        # 병렬 업로드 수행
        prefix = f"{self.user_id}/symbol_gallery"
        uploaded_files = upload_folder(upload_data, prefix, USER_DATA_BUCKET_NAME)
        
        print(f"[USER DATA] Upload {self.user_id}: {len(uploaded_files)} files")


    def download_userdata(self):
        """
        서버(GCS)의 심볼 갤러리 이미지들을 병렬 다운로드하여 로컬에 반영함.
        """
        prefix = f"{self.user_id}/symbol_gallery"
        
        # 병렬 다운로드 수행
        downloaded_files = download_folder(prefix, USER_DATA_BUCKET_NAME)
        
        if downloaded_files:
            for filename, content in downloaded_files.items():
                # 파일명에서 확장자 제거하여 키워드 추출
                if filename.lower().endswith(".png"):
                    keyword = filename[:-4] # .png 제거
                    
                    if keyword in self.symbol_gallery:
                        self.symbol_gallery[keyword].image = content
                    else:
                        # 새로운 키워드인 경우 ImageTextPair 생성하여 추가
                        self.symbol_gallery[keyword] = ImageTextPair(image=content, text=keyword)
            
            print(f"[USER DATA] Download {self.user_id}: {len(downloaded_files)} files")
        else:
             print(f"[USER DATA] Download {self.user_id}: 0 files")


