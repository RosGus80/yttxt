import os
from pprint import pprint

from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

def find_entry():

    title = 'Never gonna give you up'

    ydl_opts = {
                'outtmpl': os.path.join('%(title)s.%(ext)s'),
                'geo_bypass': True,
                'socket_timeout': 5,
            }

    search_words = set(title.lower().split())

    with YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch:{title}", download=False)['entries']

        for result in search_results:
            result_title = result['title'].lower()
            result_words = set(result_title.split())
            match_count = len(search_words & result_words)

            if match_count >= len(search_words) / 2:
                return True
            else:
                return False


