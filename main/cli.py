import argparse
import textwrap

def parse_cli_arguments():
    
    class NewlineFormatter(argparse.RawDescriptionHelpFormatter):
        def _format_action(self, action):
            parts = super()._format_action(action)
            parts = parts.split("\n")
            parts = [parts[0]] + [textwrap.fill(part, width=60) for part in parts[1:]]
            return "\n".join(parts)
        
    # This function is used to parse the command line arguments passed to the program.
    DESC = "Parse Command Line Arguments for Vinnys Terminal Ascii Player"
    EPLG = "Created by Vince Vasile - Github: https://github.com/VinnyVanGogh/vinnys-terminal-ascii-player"
    PRGRMNM = "vtap | vinnys-terminal-ascii-player"
    
    parser = argparse.ArgumentParser(description=DESC, epilog=EPLG, prog=PRGRMNM, formatter_class=NewlineFormatter)
    
    parser.add_argument("-i", "--image", help="Ex. -i '/path/to/image.png/jpg/etc'", type=str)
    
    parser.add_argument("-f", "--file", help="Ex. -f '/path/to/video.mp4'", type=str)
    
    parser.add_argument("-u", "--url", help="Ex. -u 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs'", type=str)
    
    parser.add_argument('-a', '--audio', action='store_true', help='Play audio *if -f there must be a .wav with the same name in the same dir*')
    
    parser.add_argument('-ca', '--customaudio', help='Play custom audio file', type=str)
    
    parser.add_argument('-cv', '--centervideo', action='store_true', help='Center video in terminal')
    
    parser.add_argument('-c', '--chars', default=' .,:;irsXA253hMHGS#9B&@', help='Character set to use for video', type=str)
    
    parser.add_argument('-q', '--videoquality', default='low', help='Quality of video (low, medium, high)', type=str)
    
    parser.add_argument('-C', '--colors', action='store_true', help='Use color in video')
    
    parser.add_argument('-s', '--size', nargs=2, help='Size of video in terminal (width, height) **NOTE: not working yet**', type=int)
    
    parser.add_argument('-fs', '--fullscreen', action='store_true', help='Play video in fullscreen')
    
    parser.add_argument('-S', '--speed', default=1.6, help='Speed of video', type=float)
    
    parser.add_argument('-d', '--videodirectory', help='Directory to save videos to', type=str)
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    return parser.parse_args()