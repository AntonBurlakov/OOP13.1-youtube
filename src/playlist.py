import datetime as dt
import isodate
from src.mixingetservice import MixinGetService


class PlayList(MixinGetService):
    """
    Класс для работы с PlayList
    """
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = self.get_service().playlists().list(id=self.playlist_id,
                                                        part='contentDetails,snippet',
                                                        ).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __str__(self):
        return f'{self.total_duration}'

    def get_playlist_videos(self) -> dict:
        """Возвращает ответ API на запрос всех видео плей-листа."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        _video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(_video_ids)
                                                          ).execute()
        return video_response

    @property
    def total_duration(self):
        video_response = self.get_playlist_videos()
        duration = dt.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self, ):
        playlists = self.get_playlist_videos()
        max_likes = 0
        _video_id = ''
        for video in playlists['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                _video_id = (video['id'])
        return f'\"https://youtu.be/{_video_id}\"'
