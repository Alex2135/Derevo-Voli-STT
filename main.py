import argparse

from src.yt_subtitles import download_youtube_video
from src.yt_subtitles import read_lrc
from src.yt_subtitles import read_lrc


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', help="Link to the YouTube video") 
    return parser.parse_args()


def main(config: dict):
    url = config.video  # "https://www.youtube.com/watch?v=R7nXOAm5gxU"
    mp3_file, lrc_file = download_youtube_video(url)

    text = read_lrc(lrc_file)
    output_file_path = f"{lrc_file}.txt"
    with open(output_file_path, mode="w") as output_file:
        output_file.write(text)
        print("\n")
        print(f"The output was saved to the: \"{output_file_path}\"")

    print("\n")
    print("Extracted subtitles:")
    wrapped_text = textwrap.wrap(text)
    for line in wrapped_text:
        print(line)


if __name__ == "__main__":
    config = get_config()
    
    if not config.video:
        print("There is no provided link to the video")
    else:
        main(config)

