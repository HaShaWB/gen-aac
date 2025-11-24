# user_data.py

from typing import List, Dict, Optional

from pydantic import BaseModel

from genaac.models import EditingHistory
from genaac.utils import upload_file, download_file


class UserData(BaseModel):
    user_id: str
    gallery: Optional[List[EditingHistory]] = list()

    gallery_index: Optional[Dict[str, int]] = None


    def gallery_indexing(self):
        self.gallery_index = {
            history.initial_pair.token.keyword: idx
            for idx, history in enumerate(self.gallery)
        }

    
    def get_index(self) -> Dict[str, int]:
        if self.gallery_index is None:
            self.gallery_index = self.gallery_indexing()
        return self.gallery_index


    def gallery_sorting(self):
        self.gallery.sort(key=lambda x: x.initial_pair.token.keyword)
        self.gallery_indexing()


    def add_history(self, history: EditingHistory):

        if history.initial_pair.token.keyword in self.get_index().keys():
            self.gallery[self.get_index()[history.initial_pair.token.keyword]] = history
        else:       
            self.gallery.append(history)
        self.gallery_indexing()

    
    def upload_to_server(self):
        upload_file(self.model_dump_json(), f"{self.user_id}.json", bucket_name="genaac-user-data")
        return self.user_id

    
    @staticmethod
    def from_server(user_id: str) -> Optional["UserData"]:
        data = download_file(f"{user_id}.json", bucket_name="genaac-user-data")
        if data:
            return UserData.model_validate_json(data)
        else:
            return None
