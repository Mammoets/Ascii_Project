# █ ▄▀ █▀▀▄ █▀▀▄ █▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀█ █▀▀█ █▀▀▄ █▀▀█ █▀▀▄ █▀▀█
# █ █░ █░░█ █░░█ █▄▄▀ █▄▄█ █░░█ █▄▄▀ █▄▄█ █▄▄▀ █▄▄█ █░░█ █░░█ █▄▄█ █░░█ █░░█ █░░█
# ▀ ▀▀ ▀░░▀ ▀░░▀ ▀░▀▀ ▀░░▀ ▀▀▀▀ ▀░▀▀ ▀░░▀ ▀░▀▀ ▀░░▀ ▀░░▀ ▀▀▀▀ ▀░░▀ ▀░░▀ ▀▀▀▀ ▀░░▀


import cv2
import ascii_magic
import sys
from vid_cap import get_video_capture, rescale_video, rescale_image
import time
import tempfile
import logging
from ascii_magic import AsciiArt

logger = logging.getLogger('ascii')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('ascii.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def ascii_art(args):
    video_capture, frame_time, audio_file = get_video_capture(args)
    width_ratio, height_ratio = rescale_video(video_capture, args)

    while(video_capture.isOpened()):
        current_time = time.time()
        ret, frame = video_capture.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, (width_ratio, height_ratio))
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as tmp:
            cv2.imwrite(tmp.name, resized_frame)

            if args.colors:
                ascii_frames = AsciiArt.from_image(tmp.name)
                ascii_frames.to_terminal(columns=width_ratio, char=args.chars)
            else:
                # Got color working, ascii_magic has a hard time doing grayscale though and not just white, testing out a custom grayscale function
                ascii_frames = AsciiArt.from_image(tmp.name)
                def grayscale(rgb):
                    rgb = rgb
                    r = (rgb[0])
                    g = (rgb[1])
                    b = (rgb[2])
                    brightness = (r + g + b)
                    return brightness
                
                magic_num = 255/(len(args.chars)-1.001)
                brightness = grayscale(args.chars)
                grayscale_chars = args.chars[int(brightness / magic_num)]        
                grayscale_ascii += f'\x1b[38;2;{args.chars[2]};{args.chars[1]};{args.chars[0]}m{grayscale_chars}'        
                ascii_frames.to_terminal(columns=width_ratio, char=grayscale_ascii, monochrome=True)

        while True:
            if time.time() - current_time <= frame_time:
                pass
            else:
                sys.stdout.write(f"\033[{height_ratio + 1}F") # Cursor up n lines
            break
    video_capture.release()
    
    
    
    
    
    