import os
from googleapiclient.discovery import build


class MixinGetService:

    api_key: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)
