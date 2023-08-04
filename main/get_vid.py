#TODO: Add a function that checks the video quality arg and returns the correct video quality based on the font size, ex if 1-4p font | 4k; 4-18p font | 1080p; 18p+ font | 480p 
import os
import re
import subprocess
from pytube import YouTube, extract
import logging
from pytube.extract import video_id

logger = logging.getLogger('get_vid')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('get_vid.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class AVFile:
    def __init__(self, args):
        #self.url = args.url
        self.args = args
        self.replacements = {
            "\\\\"  : chr(0x29F9),
            "[/]"   : chr(0x29F8),
            "[:]"   : chr(0xFF1A),
            "[*]"   : chr(0xFF0A),
            "[?]"   : chr(0xFF1F),
            '["]'   : chr(0xFF02),
            "[|]"   : chr(0xFF5C)
        }
    
    @staticmethod
    def multi_replace_regex(string, replacements):
        for pattern, replacement in replacements.items():
            string = re.sub(pattern, replacement, string)
        return string
    
    def get_video(self):
        self.url = self.args.url.replace('\\', '')
        yt_id = video_id(self.args.url)
        self.yt_url = f"https://www.youtube.com/watch?v={yt_id}"
        yt = YouTube(self.yt_url)
        output_directory = self.args.videodirectory or os.path.join(os.getcwd(), "videos")
        os.makedirs(output_directory, exist_ok=True)
        base_filename = os.path.join(output_directory, self.multi_replace_regex(yt.title, self.replacements))
        video_file = base_filename + '.mp4'
        mp3_file = base_filename + '.mp3'
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first().download(filename=video_file)
        audio_file = None
        if self.args.audio:
            audio_file = base_filename + '.wav'
            yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(filename=mp3_file)
            subprocess.call(["ffmpeg", "-i", mp3_file, "-ac", "2", "-f", "wav", "-y", audio_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return video_file, audio_file
    
    
    def get_video_from_file(self):
        base_filename = os.path.splitext(self.args.videodirectory)[0]
        video_file = base_filename + '.mp4'
        audio_file = None
        if self.args.audio:
            audio_file = base_filename + '.wav'
        elif self.args.customaudio:
            audio_file = self.args.customaudio
        return video_file, audio_file

    