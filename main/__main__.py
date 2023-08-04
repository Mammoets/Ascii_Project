import cv2
from cli import parse_cli_arguments
from vid_cap import get_video_capture, rescale_video
from spares.new_ascii import ascii_art, play

def main():
    args = parse_cli_arguments()
    chars = args.chars
    colors = args.colors
    video_capture, frame_time, audio_file, base_video_width, base_video_height = get_video_capture(args)
    video_size = rescale_video(args, base_video_width, base_video_height)
    print(video_size)
    print(frame_time, audio_file)
    ascii_frames, frame_time, video_capture = ascii_art(args, chars, frame, colors, video_size, video_capture)
    play(frame_time, ascii_frames, video_capture)
    
if __name__ == '__main__':
    main()