import multiprocessing
import cv2
from new_ascii import ascii_art
import threading
import pygame
import os
import time



def worker(args, video_size, image_size):
    frame, chars, colors = args
    if args.file or args.url: resized_frame = cv2.resize(frame, (video_size))
    else: resized_frame = cv2.resize(frame, (image_size))
    ascii_frame = ascii_art(args, chars, colors, video_size, image_size, frame)
    print(ascii_frame)
    return ascii_frame


def multiprocess_ascii_art(video_capture, chars, colors):
    ascii_frames_processing = []
    if not video_capture.isOpened():
        raise ValueError("in mp VideoCapture is not opened")
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        ascii_frames_processing.append(frame)
        
    video_capture.release()

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        worker_args = [(frame, chars, colors) for frame in ascii_frames_processing]
        ascii_frames = pool.map(worker(video_capture, chars, colors), worker_args)
        
    for ascii_frame in ascii_frames:
        print(ascii_frame)
    return ascii_frames


def play_audio(args, audio_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
def play(args, chars, colors, video_size, image_size, video_capture, frame_time):    
    os.system('cls' if os.name == 'nt' else 'clear')
    current_time = time.time()
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret: 
            break
        print('\x1b[H' + ascii_art(args, chars, colors, video_size, image_size, frame))
        time.sleep(frame_time)
    
        if time.time() - current_time <= frame_time:
            pass

def play_with_threading(args, video_capture, chars, colors, video_size, image_size, frame_time, audio_file):
    if args.file or args.url:
        processing_thread = threading.Thread(target=multiprocess_ascii_art, args=(video_capture, chars, colors))
        if args.audio: audio_thread = threading.Thread(target=play_audio, args=(args, audio_file))
        video_thread = threading.Thread(target=play, args=(args, chars, colors, video_size, image_size, video_capture, frame_time))
        processing_thread.start()
        time.sleep(frame_time * 100)
        video_thread.start()
        audio_thread.start()
        processing_thread.join()
        video_thread.join()
        audio_thread.join()
    else:
        pass