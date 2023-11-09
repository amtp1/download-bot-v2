import re

import requests

from bot.config import load_config

config = load_config("bot.ini")


class YouTube:
    def __init__(self, url=None):
        if url:
            self.url = url
            self.video_id = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.url)[0]

    def get_streams(self, is_audio=None, is_video=None):
        url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"

        querystring = {"videoId": self.video_id}

        headers = {
            "X-RapidAPI-Key": config.rapid.token,
            "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        response = response.json()

        if is_audio:
            audios = {"title": response["title"], "audios": response["audios"]}
            return audios
        elif is_video:
            videos = {"title": response["title"], "videos": response["videos"]}
            return videos

    def download(self, url: str):
        response = requests.get(url=url, stream=True)
        return response.content
