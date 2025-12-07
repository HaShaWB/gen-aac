# demo/user_data.py

import hashlib
from typing import Dict

import streamlit as st
from pydantic import BaseModel

from genaac.utils import ImageTextPair, download_folder, upload_folder, upload_file, make_id
from genaac.config import CONFIG
from genaac.aac_from_keyword import aac_from_keyword
from genaac.convert_keyword import convert_keyword


USER_DATA_BUCKET_NAME = CONFIG["database"]["user_data_bucket_name"]


def get_user_hash() -> str:
    """
    접속한 유저의 브라우저 정보(User-Agent)와 IP를 기반으로 식별 해시를 생성한다.
    """
    # Streamlit 컨텍스트에서 클라이언트 정보 추출
    headers = st.context.headers
    
    if headers is None:
        return "unknown_user"
        
    # 식별에 사용할 정보 조합 (IP + 브라우저 정보)
    remote_ip = headers.get("X-Forwarded-For", "127.0.0.1")
    user_agent = headers.get("User-Agent", "unknown_agent")
    
    unique_str = f"{remote_ip}_{user_agent}"
    
    # SHA256으로 해싱하여 짧은 ID 생성
    return hashlib.sha256(unique_str.encode()).hexdigest()[:12]


class UserData(BaseModel):
    user_id: str = get_user_hash()
    symbol_gallery: Dict[str, ImageTextPair] = {}


    def regenerate_symbol(self, keyword: str, converting_keyword: bool = True):
        pair = aac_from_keyword(keyword, converting_keyword=converting_keyword)
        self.add_symbol(pair)
        upload_file(pair.image, f"{keyword}/{make_id()}.png")
        return pair


    def find_or_generate_symbol(self, keyword: str):
        keyword = convert_keyword(keyword)
        if keyword in self.symbol_gallery:
            return self.symbol_gallery[keyword]
        else:
            return self.regenerate_symbol(keyword, converting_keyword=False)

    def add_symbol(self, pair: ImageTextPair):
        self.symbol_gallery[pair.text] = pair
        self.upload_symbol(pair.text)

    
    def upload_symbol(self, keyword):
        pair = self.symbol_gallery[keyword]
        data = {f"{keyword}.png": pair.image}
        prefix = f"{self.user_id}/symbol_gallery"
        upload_folder(data, prefix, USER_DATA_BUCKET_NAME)
        
        print(f"[USER DATA] Upload {self.user_id}: {keyword}")


    def upload_server(self):
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


    def download_server(self):
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


