import cv2
import numpy as np
import time
import os
import pygame

def colorize_ascii_art(char, rgb):
    if isinstance(rgb, int) or isinstance(rgb, np.uint8):
        r = g = b = int(rgb)
    else:
        b, g, r = map(int, rgb)
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

def ascii_art(args, chars, colors, video_size, image_size, frame):
        if args.file or args.url:
            resized_frame = cv2.resize(frame, (video_size))
            f = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif args.image:
            resized_frame = cv2.resize(frame, (image_size))
            f = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        area = 255 // (len(chars) - 1) if len(chars) > 1 else 255

        def mapping_pixels(pixels=None):
            pixels = zip(pixels[0], pixels[1])
            return ''.join(list(map(lambda p: colorize_ascii_art(chars[p[0]//area % len(chars)], p[0]) if not colors else colorize_ascii_art(chars[p[0]//area % len(chars)], p[1]), pixels)))
        
        ascii_frames = list(map(mapping_pixels, zip(f, resized_frame)))
        ascii_frames = '\n'.join(ascii_frames)
        return ascii_frames
    
def play_audio(audio_filename_wav):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename_wav)
    pygame.mixer.music.play()

def play(args, chars, colors, video_size, image_size, video_capture, frame_time, audio_filename_wav):
    os.system('cls' if os.name == 'nt' else 'clear')
    current_time = time.time()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename_wav)
    pygame.mixer.music.play()
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret: 
            break
        print('\x1b[H' + ascii_art(args, chars, colors, video_size, image_size, frame))
        time.sleep(frame_time)
    
        if time.time() - current_time <= frame_time:
            pass
   

    

            