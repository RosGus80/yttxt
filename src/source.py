import json
import os
import re

import requests
from yt_dlp import YoutubeDL
from requests.exceptions import ConnectionError


error_messages = {
    'connection': '[generic] Unable to download webpage: <urllib3.connection.HTTPSConnection',
    'invalid_url': "[generic] 'title' is not a valid URL.",
    'unsupported_url': 'Unsupported URL:',
    'page_not_found': '[generic] Unable to download webpage:',
    'timeout': 'Read timed out.',
    'post_hook': 'takes 0 positional arguments but 1 was given',
}


class YoutubeDownloader:

    class DownloaderLogger:

        def error(msg):
            if not error_messages['post_hook'] in msg and not error_messages['timeout'] in msg:
                print('ERROR: ' + msg)

        def warning(msg):
            pass

        def debug(msg):
            pass

    class DebuggingLogger:

        def error(msg):
            if error_messages['post_hook'] in msg:
                print('[debug] ERROR (CAUSED INTENTIONALLY AS A PART OF A CODE LOGIC): ' + msg)
            else:
                print('[debug] ERROR: ' + msg)

        def warning(msg):
            print('[debug] WARNING: ' + msg)

        def debug(msg):
            print('[debug] DEBUG: ' + msg)

    @staticmethod
    def find_json(title, max_results=1) -> dict:
        from youtube_search import YoutubeSearch

        results = json.loads(YoutubeSearch(title, max_results=max_results).to_json())

        return results

    def get_search_links(self, title, max_results=1) -> list:
        json_search = self.find_json(title=title, max_results=max_results)
        link_prefix = 'https://www.youtube.com'
        links = [link_prefix + video['url_suffix'] for video in json_search['videos']]

        return links

    def extract_urls_from_txt(self, txt_file, no_check=False) -> list:
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

        with open(txt_file, 'r', encoding='utf-8') as f:
            output_links = []
            for line in f.readlines():
                if url_pattern.search(line) is None:
                    video_link = self.get_search_links(title=line, max_results=1)[0]
                    output_links.append(video_link)
                else:
                    video_link = line
                    not_found = f'Video by link {line.strip()} not found'

                if no_check:
                    output_links.append(video_link)
                else:
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
        print(f'Downloaded: {d["_percent_str"]}')

    @staticmethod
    def post_hook():
        """Post hook is used solely to raise an exception in case he is called,
        because this is used for breaking the loops of downloading"""
        return 0

    def get_video_info(self, url) -> dict:
        print('Extracting page info...')
        ydl_opts = {'quiet': True,
                    'restrictfilenames': True,
                    'trim_file_names': True,
                    'windowsfilenames': True,
                    'logger': self.DownloaderLogger}

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info

    def download(self, url, output_dir: str = '', audio_only=False, debugging=False) -> tuple[str, str]:
        print(f'Downloading: {url}')

        ydl_opts = {
            'post_hooks': [self.post_hook],
            'outtmpl': os.path.join(output_dir, '%(title)s'),
            'geo_bypass': True,
            'socket_timeout': 5,
            'quiet': True,
            'restrictfilenames': True,
            'trim_file_names': True,
            'windowsfilenames': True,
            # 'cookiesfrombrowser': 'safari',
        }

        if debugging:
            ydl_opts['logger'] = self.DebuggingLogger
        else:
            ydl_opts['logger'] = self.DownloaderLogger
            ydl_opts['progress_hooks'] = [self.progress_hook]

        info = self.get_video_info(url)
        video_title = info['title']

        if audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
            with YoutubeDL(ydl_opts) as ydl:
                for i in range(40):
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
                            logging_tuple = (video_title, f"Couldn't download audio. Error: {e}")
                            break
                else:
                    logging_tuple = (video_title, f"Couldn't download audio. Error: timeout error")
                    print(f'Timeout error while downloading {video_title}. Please, check your internet connection')
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]'
            ydl_opts['socket_timeout'] = 20
            ydl_opts['fragment_retries'] = 10
            ydl_opts['merge_output_format'] = 'mp4'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

            with YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except Exception as e:
                    if error_messages['post_hook'] in str(e):
                        print(f'Video {video_title} has been downloaded')
                        logging_tuple = (video_title, 'Successful')
                    else:
                        logging_tuple = (video_title, f"Couldn't download video. Error: {e}")

        return logging_tuple

    def download_from_txt(self, txt_file, output_dir='', audio_only=False, debugging=False, no_check=False):
        """Main func for downloading videos from a file"""
        links = self.extract_urls_from_txt(txt_file, no_check=no_check)
        # TODO: Ask user if all the links from the file are correct (if title ask title: link? If link, print link: valid/invalid)

        logging_dict = {}
        for link in links:
            log = self.download(link, output_dir=output_dir, audio_only=audio_only, debugging=debugging)
            logging_dict[log[0]] = log[1]

        return logging_dict

