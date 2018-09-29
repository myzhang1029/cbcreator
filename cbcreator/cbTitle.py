from PIL import Image, ImageDraw, ImageFont
from random import randint
import cbResize

def create(bgfile, title, fontfile=""):
    """Create a title slide.
    bgfile: filename of the background picture
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    draw = ImageDraw.Draw(image)
    color = image.getcolors()
    if fontfile == "":
        fontfile = "fonts/{:03}.ttf".format(randint(1, 4))
    print(fontfile)
    for size in range(344, 1):
        font = ImageFont.truetype(fontfile, size, encoding="unic")
        # not too large
        if not ImageDraw.textsize(title, font=font) > 2948:
            draw.text((500,200), title, font=font)
            return image
    # should not reach here
    return image
