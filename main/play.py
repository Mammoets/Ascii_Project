#TODO: Write the code
import pygame
import time
import os
from new_ascii import ascii_art

def play_audio(audio_filename_wav):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename_wav)
    pygame.mixer.music.play()

def play(args, chars, colors, video_size, image_size, video_capture, frame_time, audio_filename_wav):
    os.system('cls' if os.name == 'nt' else 'clear')
    current_time = time.time()
    play_audio(audio_filename_wav)
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret: 
            break
        print('\x1b[H' + ascii_art(args, chars, colors, video_size, image_size, frame))
        time.sleep(frame_time)
    
        if time.time() - current_time <= frame_time:
            pass