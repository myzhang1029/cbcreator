from PIL import Image, ImageDraw, ImageFont
from random import randint
import cbResize
import cbColor

def create(bgfile, title, fontfile=""):
    """Create a title slide.
    bgfile: filename of the background picture
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    avgcolor = cbColor.avgcolor(image)
    compcolor = cbColor.compcolor(avgcolor)
    draw = ImageDraw.Draw(image)
    if fontfile == "":
        fontfile = "fonts/{:03}.ttf".format(randint(1, 4))
    font = ImageFont.truetype(fontfile, 600, encoding="unic")
    size = draw.textsize(title, font=font)
    left = (2948 - size[0]) // 2
    top = (3401 - size[1]) // 2
    draw.text((left, top), title, font=font, fill=compcolor)
    return image
    # should not reach here
    return image
