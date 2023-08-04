from cli import parse_cli_arguments
from vid_cap import get_video_capture, rescale_video, rescale_image
from new_ascii import play

def main():
    args = parse_cli_arguments()
    chars = args.chars
    colors = args.colors
    video_capture, frame_time, audio_file, base_video_width, base_video_height = get_video_capture(args)
    video_size = rescale_video(args, base_video_width, base_video_height)
    image_size = rescale_image(args.image, args)
    play(args, chars, colors, video_size, image_size, video_capture, frame_time, audio_file)
    
if __name__ == '__main__':
    main()