import cv2
import numpy as np


def colorize_ascii_art(char, rgb):
    if isinstance(rgb, int) or isinstance(rgb, np.uint8):
        r = g = b = int(rgb)
    else:
        b, g, r = map(int, rgb)
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"


def ascii_art(args, video_size, image_size, frame):
    if args.file or args.url:
        resized_frame = cv2.resize(frame, (video_size))
        f = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif args.image:
        resized_frame = cv2.resize(frame, (image_size))
        f = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    area = 255 // (len(args.chars) - 1) if len(args.chars) > 1 else 255

    def mapping_pixels(pixels=None):
        pixels = zip(pixels[0], pixels[1])
        if not args.colors:
            return ''.join(list(map(lambda p: colorize_ascii_art(
                args.chars[p[0]//area % len(args.chars)], p[0]), pixels)))
        else:
            return ''.join(list(map(lambda p: colorize_ascii_art(
                args.chars[p[0]//area % len(args.chars)], p[1]), pixels)))
    ascii_frames = list(map(mapping_pixels, zip(f, resized_frame)))
    ascii_frames = '\n'.join(ascii_frames)
    return ascii_frames
