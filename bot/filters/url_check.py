import re


def check_url(url: str):
    youtube_regex = (
        r"(https?://)?(www\.)?"
        r"(youtube|youtu|youtube-nocookie|music.youtube)\.(com|be)/"
        r"(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    tiktok_regex = (r'https?://(www\.)?tiktok\.com/@\w+/video/\d+')
    youtube_regex_match = re.match(youtube_regex, url)
    tiktok_regex_match = re.match(tiktok_regex, url)
    if youtube_regex_match:
        return {'service': 'youtube', 'url': youtube_regex_match}
    elif tiktok_regex_match:
        return {'service': 'tiktok', 'url': tiktok_regex_match}
