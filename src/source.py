import json
import os
import re

import requests
import yt_dlp
from requests.exceptions import ConnectionError
import logging

# logging.basicConfig(level=logging.DEBUG, filename='.log')


error_messages = {
    'connection': 'ERROR: [generic] Unable to download webpage: <urllib3.connection.HTTPSConnection',
    'invalid_url': "ERROR: [generic] 'title' is not a valid URL.",
    'unsupported_url': 'ERROR: Unsupported URL:',
    'page_not_found': 'ERROR: [generic] Unable to download webpage:',
    'timeout': 'Read timed out.',
    'post_hook': 'takes 0 positional arguments but 1 was given',
}


class YoutubeDownloader:

    @staticmethod
    def find_json(title, max_results=1):
        from youtube_search import YoutubeSearch

        results = json.loads(YoutubeSearch(title, max_results=max_results).to_json())

        return results

    def get_search_links(self, title, max_results=1):
        json_search = self.find_json(title=title, max_results=max_results)
        link_prefix = 'https://www.youtube.com'
        links = [link_prefix + video['url_suffix'] for video in json_search['videos']]

        return links

    def extract_urls_from_txt(self, txt_file):
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

        with open(txt_file, 'r') as f:
            output_links = []
            for line in f.readlines():
                if url_pattern.search(line) is None:
                    video_link = self.get_search_links(title=line, max_results=1)[0]
                    output_links.append(video_link)
                else:
                    video_link = line
                    not_found = f'Video by link {line.strip()} not found'

                    try:
                        response = requests.get(video_link)
                    except ConnectionError:
                        print(not_found)
                        continue
                    if response.status_code == 200:
                        output_links.append(video_link)
                    else:
                        print(not_found)

            return output_links

    @staticmethod
    def progress_hook(d):
        print(d['_percent_str'])

    @staticmethod
    def post_hook():
        """Post hook is used solely to raise an exception in case he is called,
        because this is used for breaking the loops of downloading"""
        return 0

    @staticmethod
    def get_video_info(url):
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info

    def download(self, url, output_dir: str = '', audio_only=False) -> tuple[str, str]:
        print(f'Downloading: {url}')

        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'post_hooks': [self.post_hook],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'geo_bypass': True,
            'socket_timeout': 5,
        }

        info = self.get_video_info(url)
        video_title = info['title']

        if audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for i in range(20):
                    try:
                        ydl.download([url])
                    except Exception as e:
                        if error_messages['timeout'] in str(e):
                            continue
                        elif error_messages['post_hook'] in str(e):
                            print(f'Video {video_title} has been downloaded')
                            logging_tuple = (video_title, 'Successful')
                            break
                        else:
                            logging_tuple = (video_title, f"Couldn't download video. Error: {e}")
                            break
                else:
                    print(f'Timeout error while downloading {video_title}. Please, check your internet connection')
        else:
            raise Exception('Video download is not implemented yet')
            # TODO: video downloading implementation
            # ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
            # ydl_opts['socket_timeout'] = 20
            # ydl_opts['fragment_retries'] = 10
            # ydl_opts['retries'] = 10
            # ydl_opts['postprocessors'] = [{
            #     'key': 'FFmpegMerger',
            # }]
            # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #     try:
            #         ydl.download([url])
            #     except Exception as e:
            #         if error_messages['post_hook'] in str(e):
            #             print(f'Video {video_title} has been downloaded')
            #         else:
            #             raise e

        return logging_tuple

    def download_from_txt(self, txt_file, output_dir='', audio_only=False):
        """Main func for downloading videos from a file"""
        links = self.extract_urls_from_txt(txt_file)
        logging_dict = {}
        for link in links:
            log = self.download(link, output_dir=output_dir, audio_only=audio_only)
            logging_dict[log[0]] = log[1]

        return logging_dict


# downloaderobj = YoutubeDownloader()
# # downloaderobj.download(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUYTmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAK',
# #                        output_dir='downloads', audio_only=True)
#
# links = downloaderobj.extract_urls_from_txt('downloader/songs.txt')
# downloaderobj.download_from_txt('downloader/songs.txt', output_dir='downloads', audio_only=True)
