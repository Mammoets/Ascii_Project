import multiprocessing
import cv2
import colorama
import queue
import pygame
import os
# import time
from collections import deque
from new_ascii import ascii_art
from multiprocessing.pool import ThreadPool
from vid_cap import rescale_video, rescale_image
from get_vid import get_video, get_video_from_file

colorama.init()
INPUT_BUFFER = queue.Queue()


def processing(frame_time):
    while True:
        frame = INPUT_BUFFER.get()
        print('\x1b[H' + frame)
        ch = cv2.waitKey(1)
        if ch == 27:
            break


def play_with_threading(args):
    pending = deque()
    thread_count = multiprocessing.cpu_count()
    pool = ThreadPool(processes=thread_count)
    if args.file:
        video_file, audio_file = get_video_from_file(args.file, args)
    else:
        video_file, audio_file = get_video(args.url, args) 

    video_capture = cv2.VideoCapture(video_file)
    # frames_per_second = video_capture.get(cv2.CAP_PROP_FPS)
    # frame_time = 1 / frames_per_second
    base_video_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    base_video_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_size = rescale_video(args, base_video_width, base_video_height)
    image_size = rescale_image(args.image, args)
    play_audio(audio_file)
    frame_count = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        while len(pending) > 0:
            frame_count += 1
            res = pending.popleft().get()
            print('\x1b[H' + res)
        if len(pending) < thread_count:
            ret, frame = video_capture.read()
            if not ret:
                break
            task = pool.apply_async(ascii_art, (args, video_size,
                                                image_size, frame.copy()))
            pending.append(task)
        ch = cv2.waitKey(1)
        if ch == 27:
            break


def play_audio(audio_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
