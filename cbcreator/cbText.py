from PIL import Image, ImageDraw, ImageFont
from random import randint
import cbResize
import cbColor

def create(bgfile, txtfile, title, fonttxt="", fontitle=""):
    """Create a text slide.
    bgfile: filename of the background picture
    txtfile: filename of the content
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    avgcolor = cbColor.avgcolor(image)
    compcolor = cbColor.compcolor(avgcolor)
    draw = ImageDraw.Draw(image)
    if fonttxt == "":
        fonttxt = "fonts/{:03}.ttf".format(randint(1, 4))
    if fontitle == "":
        fontitle = "fonts/{:03}.ttf".format(randint(1, 4))
        if fonttxt == fontitle:
            # Retry once, if it's still the same, ignore it
            fontitle = "fonts/{:03}.ttf".format(randint(1, 4))
    fontx = ImageFont.truetype(fonttxt, 300, encoding="unic")
    fontt = ImageFont.truetype(fontitle, 600, encoding="unic")
    size = draw.textsize(title, font=fontt)
    left = (2661 - size[0]) // 2
    top = (3072 - size[1]) // 2
    draw.text((left, top), title, font=fontt, fill=compcolor)
    draw.text((left, top), unicode(open(txtfile).read(), "UTF-8"), font=fontx, fill=compcolor)
    return image
