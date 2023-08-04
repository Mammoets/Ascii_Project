import ascii_magic
from ascii_magic import AsciiArt

output = AsciiArt.from_image(
    '/Users/vincevasile/Desktop/71173137607__D04D09DC-0022-4D77-8FAE-0E8E190DBCAD.jpg',
)
output.to_terminal(columns=100, char='█')