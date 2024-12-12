def main():
    from src.source import YoutubeDownloader

    import argparse

    parser = argparse.ArgumentParser(
                    prog='YTTXT',
                    description='Small convenient interface for downloading videos using yt-dlp, hopefully providing '
                                'several cool options to make its usage easier',
                    usage='yttxt [OPTIONS] [ARGUMENTS]')

    parser.add_argument('-u', '--url', type=str, help="Pass the video URL after the flag to download this video "
                                                      "(put the url into the quotation marks)."
                                                      "Cant't be used simultaneously with the -f flag ", required=False)
    parser.add_argument('-f', '--file', type=str, help="Pass the path to a file with video URLs/thumbnails, "
                                                       "each on a separate line (can't be used with -u flag)",
                        required=False)
    parser.add_argument('-o', '--output', type=str, help='Pass the path to the output directory after this flag',
                        required=False)
    parser.add_argument('-a', '--audio', action='store_true', help='If passed, only audios will be downloaded '
                                                                   '(False by default)', required=False)
    parser.add_argument('-d', '--debug', action='store_true', help='If passed, the downloader will print all the log '
                                                                   'info he gets to the terminal')

    args = parser.parse_args()

    if args.url and args.file:
        print('Cant\'t use -u and -f flags at the same time')
        exit()

    downloader = YoutubeDownloader()

    if not args.output:
        args.output = ''

    if args.url:
        log = downloader.download(args.url, output_dir=args.output, audio_only=args.audio, debugging=args.debug)
        print(f'{log[0]} : {log[1]}')
    elif args.file:
        log = downloader.download_from_txt(args.file, output_dir=args.output, audio_only=args.audio,
                                           debugging=args.debug)
        print(f'the downloading has been finished.')
        for k, v in log.items():
            print(f'{k} : {v}')
    else:
        print("Pass either -u or -f flag so i know what you want to do. If you need help, type 'yttxt -h'")


if __name__ == '__main__':
    main()
