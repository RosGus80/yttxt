import os

from setuptools import setup, find_packages

if os.system("ffmpeg -version"):
    raise LookupError(
        "yttxt is an interface for the yt-dlp package and it uses ffmpeg. Please, install ffmpeg to proceed."
        "The instruction is on yttxt github page.a"
    )

setup(
    name='YTTXT',
    version='0.0.1',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'Requests==2.32.3',
        'setuptools==65.5.0',
        'youtube_search==2.1.2',
        'yt_dlp==2024.12.6',
    ],
    entry_points={'console_scripts': ['yttxt=src.main:main']},
)
