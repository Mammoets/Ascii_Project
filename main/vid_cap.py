import cv2
import shutil
from get_vid import get_video, get_video_from_file

def get_video_capture(args):
    if args.file:
        video_file, audio_file = get_video_from_file(args.file, args)
    else:
        video_file, audio_file = get_video(args.url, args)   
        
    video_capture = cv2.VideoCapture(video_file)
    frames_per_second = video_capture.get(cv2.CAP_PROP_FPS)
    frame_time = 1 / frames_per_second
    base_video_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    base_video_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return video_capture, frame_time, audio_file, base_video_width, base_video_height

def rescale_video(args, base_video_width, base_video_height):
    if args.url or args.file:
        terminal_width, terminal_height = shutil.get_terminal_size()
        
        if terminal_width % 2 != 0:
            terminal_width -= 1
        if terminal_height % 2 != 0:
            terminal_height -= 1
        
        if args.fullscreen:    
            width_ratio = terminal_width 
            height_ratio = terminal_height 
            video_size = (width_ratio, height_ratio)
        else:
            width_ratio = terminal_width / base_video_width
            height_ratio = terminal_height / base_video_height
            scale_factor = min(width_ratio, height_ratio)
            width_ratio = int(scale_factor * base_video_width)
            height_ratio = int(scale_factor * base_video_height)
            video_size = (width_ratio, height_ratio)
        return video_size

def rescale_image(image: str, args):
    if args.image:
        image=cv2.imread(args.image)
        terminal_width, terminal_height = shutil.get_terminal_size()
        base_image_width = image.shape[1]
        base_image_height = image.shape[0]
        
        if terminal_width % 2 != 0:
            terminal_width -= 1
        if terminal_height % 2 != 0:
            terminal_height -= 1
            
        if args.fullscreen:
            width_ratio = terminal_width
            height_ratio = terminal_height
            image_size = (width_ratio, height_ratio)
        else:
            width_ratio = terminal_width / base_image_width
            height_ratio = terminal_height / base_image_height
            scale_factor = min(width_ratio, height_ratio)
            width_ratio = int(scale_factor * base_image_width)
            height_ratio = int(scale_factor * base_image_height)
            image_size = (width_ratio, height_ratio)
        return image_size