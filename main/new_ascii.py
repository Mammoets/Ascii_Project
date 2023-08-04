import cv2
import numpy as np

class AsciiArt:

    def __init__(self, args, frame, frame_size):
        self.args = args
        self.frame = frame
        self.frame_size = frame_size

    def colorize_ascii_art(self, char, rgb):
        if isinstance(rgb, int) or isinstance(rgb, np.uint8):
            r = g = b = int(rgb)
        else:
            b, g, r = map(int, rgb)
        return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

    def calculate_area(self):
        self.area = 255 // (len(self.args.chars) - 1) if len(self.args.chars) > 1 else 255

    def colorize_and_map(self, pixel):
        char_index = pixel[0] // self.area % len(self.args.chars)
        rgb_value = pixel[1] if self.args.colors else pixel[0]
        return self.colorize_ascii_art(self.args.chars[char_index], rgb_value)

    def mapping_pixels(self, pixels):
        pixels = zip(pixels[0], pixels[1])
        return ''.join(list(map(self.colorize_and_map, pixels)))

    def ascii_art(self):
        resized_frame = cv2.resize(self.frame, (self.frame_size))
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.calculate_area()

        ascii_frame = list(map(self.mapping_pixels, zip(gray_frame, resized_frame)))
        ascii_frame = '\n'.join(ascii_frame)
        return ascii_frame

