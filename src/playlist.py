from datetime import datetime

import isodate

from helper.youtube_api_manual import youtube, video_ids, video_id
from src.mixingetservice import MixinGetService
from src.video import Video


class PlayList(MixinGetService):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             ).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __str__(self):
        return f'{self.total_duration}'

    @property
    def total_duration(self):
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        # printj(video_response)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            return duration

    def show_best_video(self, ):
        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             ).execute()
        for video in playlists['items']:
            qw = video['statistics']['likeCount']
            return qw
