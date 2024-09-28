import re
import urllib3
import logging
from urllib3.util.retry import Retry

import requests

from bot.config import load_config

config = load_config("bot.ini")
logging.getLogger("urllib3").setLevel(logging.WARNING)


class TikTok:
    def __init__(self, url=None):
        if url:
            self.url = url
            self.video_id = re.findall(r"(?:|shareId=^)\d{19}", self.url)[0]
            self.author = None

    def get_video_url(self):
        url = f"https://tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com/video/{self.video_id}"
        headers = {
            "x-rapidapi-key": config.rapid.tiktok_token,
            "x-rapidapi-host": "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        self.author = response.json()['data']['aweme_detail']['author']['nickname']
        video_url = response.json()['data']['aweme_detail']['video']['download_addr']['url_list'][-1]
        return video_url

    def download(self):
        http = urllib3.PoolManager()
        response = http.request('GET', self.get_video_url())
        return {'author': self.author, 'data': response.data}
