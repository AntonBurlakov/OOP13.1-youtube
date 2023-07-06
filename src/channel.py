import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.custom_url = self.channel['items'][0]['snippet']['customUrl']
        self.url = f'https://www.youtube.com/{self.custom_url}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title}({self.url}){self.subscriber_count}'

    def __add__(self, other):
        return int(int(self.subscriber_count) + int(other.subscriber_count))

    def __sub__(self, other):
        return int(int(self.subscriber_count) - int(other.subscriber_count))

    def __lt__(self, other):
        """Метод для операции сравнения «меньше» """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Метод для операции сравнения «меньше
        или равно"""
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        """Метод для операции сравнения «больше» """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Метод для операции сравнения «больше
        или равно»"""
        return self.subscriber_count >= other.subscriber_count

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, path):
        data = self.__dict__
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
