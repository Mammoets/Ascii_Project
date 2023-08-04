import cv2
import shutil


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