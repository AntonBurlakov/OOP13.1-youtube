
from helper.youtube_api_manual import youtube
from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video = Video.get_service().videos().list(id=video_id, part='snippet,statistics').execute()
        self.id = self.video['items'][0]['id']
        self.title_video = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.moscowpython.ru/meetup/14/gil-and-python-why/'
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title_video}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
