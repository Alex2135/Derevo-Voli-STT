import os
import re

import youtube_dl


class FilenameCollectorPP(youtube_dl.postprocessor.common.PostProcessor):
    def __init__(self, ext="lrc"):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []
        self.ext = ext

    def run(self, information):
        self.filenames.append(information['filepath'])
        filename, ext = os.path.splitext(information['filepath'])
        self.filenames.append(f"{filename}.en.{self.ext}")
        return [], information


def download_youtube_video_subtitles(url: str, with_auto_subtitles: bool = False) -> FilenameCollectorPP:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegSubtitlesConvertor',
            "format": "lrc"
        }],

    }
    if with_auto_subtitles:
        ydl_opts.update({
            'writeautomaticsub': True,
            'subtitleslangs': ['en']
        })
    else:
        ydl_opts.update({
            'writesubtitles': True,
            'subtitleslangs': ['en']
        })
    filename_collector = FilenameCollectorPP(
        ext=ydl_opts["postprocessors"][1]["format"]
    )
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(filename_collector)
        info = ydl.extract_info(url, download=False)
        ydl.download([url])
    return filename_collector.filenames


def download_youtube_video(url: str) -> list:
    print("Trying to download video with the user's provided subtitles")
    resulted_files = download_youtube_video_subtitles(url)
    if os.path.exists(resulted_files[1]):  # If exists .lrc file
        return resulted_files
    else:
        print("Trying to download video with the auto-generated subtitles")
        resulted_files = download_youtube_video_subtitles(url, True)
    return resulted_files


def read_lrc(filename: str) -> str:
    lrc_file = open(filename)
    lrc_string = ''.join(lrc_file.readlines())
    lrc_file.close()

    lirics = re.sub(r"\[.*?\]", "", lrc_string)  # remove the brackets and inner content
    lirics = lirics.replace("\n", " ").strip()   # remove new line signs with leading and trailing whitespaces
    lirics = ' '.join(lirics.split())            # remove double and tripple whitespaces
    return lirics

