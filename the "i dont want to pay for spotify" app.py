#make a stupid playlist on youtube and download it as mp3 hhhhhh
# MAKE THE PLAYLIST PUBLIC FOR GODS SAKE !!!!!!!!!!!!

import os
import yt_dlp


# Paste your YouTube playlist link or individual video links here
URLS = [
    "https://www.youtube.com/watch?v=_eACTXi1DTc&list=PLK1zi0okv7QI"
]

# name of the folder where your MP3s will be saved
DOWNLOAD_FOLDER = "Music"


def download_audio(urls, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '160',  # dont change it doent matter
        }],
        'ignoreerrors': True,  # skips broken/deleted videos in a playlist without stopping
        'noplaylist': False,   # allows playlist processing
    }

    print(f"Starting download to: {os.path.abspath(output_folder)}\n")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    
    print("\nAll done! Check your music folder.")

if __name__ == "__main__":
    download_audio(URLS, DOWNLOAD_FOLDER)



