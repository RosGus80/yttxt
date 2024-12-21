# YTTXT - YouTube video/audio downloader terminal interface for yt-dlp (WIP version - many features are far from working)

## This package provides you with the convenient CLI for yt-dlp library, providing you with features like downloading videos/audios from a txt file and not needing to do any extra work (don't bother about time-out retries or ffmpeg work - it is presumably properly done by yttxt)

## Installment instructions:
* ### Install ffmpeg - yt-dlp uses ffmpeg for postprocessing videos and probably will not work without ffmpeg installed.

* #### <span style="color:cyan"> For Windows: tutorial here: https://phoenixnap.com/kb/ffmpeg-windows </span>
* #### <span style="color:cyan"> For mac: </span> ``brew install ffmpeg``
* #### <span style="color:cyan"> For Linux: </span> ``sudo apt install ffmpeg``

* ### Then make sure that ffmpeg is installed by running ``ffmpeg -version`` in your terminal. It should provide some output.
* ### Then make sure that python is installed on your computer by running ``whichpython``. If python is not installed, install it from https://www.python.org/downloads/
* #### If ffmpeg and python are installed on your computer, run ``python3 -m pip install --upgrade git+https://github.com/RosGus80/yttxt`` or, for Windows, ``py -m pip install --upgrade git+https://github.com/RosGus80/yttxt``
* ### Then you should be able to call yttxt from terminal by running ``yttxt -[flag] [argument]`` (see 'usage' for instructions)
* #### If you want to update your yttxt package, you should run ``python3 -m pip install --upgrade --force-reinstall git+https://github.com/RosGus80/yttxt`` or ``py -m pip install --upgrade --force-reinstall git+https://github.com/RosGus80/yttxt`` for Windows

## Usage 

#### You should call this module by running ``yttxt -[flag] [argument]``. For help, you should run ``yttxt -h`` and check all the valid flags.
#### If you want to download one video, you may pass the URL by running ``yttxt -u URL`` (replace URL by actual video URL)
#### If you want to download videos from a text file, you should create a text file that would contain either a url or a thumbnail on each line (be careful: if you pass a thumbnail, yttxt will automatically download first video in search by this request) and run ``yttxt -f path-to-file``
#### If you only want to download audio (mp3) files and not video files, pass the -a flag (with no arguments) along with others. 
#### If you want to specify the output folder for the downloaded files (recommended to do), pass the -o flag. Example: ``yttxt -a -f songs.txt -o downloads``
#### If you need to get a glimpse on how to program is working and/or open an issue, you would be interested in seeing all the debugging info that yt-dlp provides. In this case, pass the -d flag while calling yttxt
#### Yttxt checks if the link from the file is valid or not. It takes some extra time for the request, but if you don't want it to validate links this way before the downloading process, pass the --no-check flag.
