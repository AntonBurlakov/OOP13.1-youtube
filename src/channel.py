import json
import os

from src.mixingetservice import MixinGetService


class Channel(MixinGetService):
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

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

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def to_json(self, path):
        data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
