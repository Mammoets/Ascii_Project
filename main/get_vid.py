#TODO: Add a function that checks the video quality arg and returns the correct video quality based on the font size, ex if 1-4p font | 4k; 4-18p font | 1080p; 18p+ font | 480p 
import os
import re
import subprocess
from pytube import YouTube, extract
import logging

logger = logging.getLogger('get_vid')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('get_vid.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def multi_replace_regex(string, replacements):
    for pattern, replacement in replacements.items():
        string = re.sub(pattern, replacement, string)
    return string

replacements = {
    "\\\\"  :   chr(0x29F9),
    "[/]"   :   chr(0x29F8),
    "[:]"   :   chr(0xFF1A),
    "[*]"   :   chr(0xFF0A),
    "[?]"   :   chr(0xFF1F),
    '["]'   :   chr(0xFF02),
    "[|]"   :   chr(0xFF5C)
}

def get_video(url: str, args):
    url = args.url
    url = url.replace('\\', '')
    yt_id = extract.video_id(url)
    yt_url = f"https://www.youtube.com/watch?v={yt_id}"
    yt = YouTube(yt_url)
    output_directory = None
    
    if args.videodirectory:
        output_directory = args.videodirectory
    else:
        output_directory = os.path.join(os.getcwd(), "videos")
        
    os.makedirs(output_directory, exist_ok=True)
    video_file = os.path.join(output_directory, multi_replace_regex(yt.title, replacements) + '.mp4')
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first().download(filename=video_file)
    
    if args.audio:
        base_file = os.path.splitext(video_file)[0]
        mp3_file = base_file + '.mp3'
        audio_file = base_file + '.wav'
        
        yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(filename=mp3_file)  
        subprocess.call(["ffmpeg", "-i", f"{mp3_file}", "-ac", "2", "-f", "wav", "-y", f"{audio_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(mp3_file)
    return video_file, audio_file

def get_video_from_file(file: str, args):
    video_file = file    
    if args.audio:
        audio_file = os.path.splitext(video_file)[0] + '.wav'
    if args.customaudio:
        audio_file = args.customaudio
    return video_file, audio_file

    
    
    
    
    
    
    
    

    

    
    
    