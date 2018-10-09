from PIL import Image, ImageDraw, ImageFont
from random import randint
import cbResize
import cbColor

def autowrap(text, width, draw, font):
    initsz = draw.textsize(text, font=font)[0]
    txtlen = len(text)
    # shouldn't split a character into two
    wraploc = initsz // width - 1
    resultstr = ""
    for idx in range(0, txtlen):
        if idx % wraploc == 1:
            resultstr += '\n'
        resultstr += text[idx]
    return resultstr

def create(bgfile, txtfile, title, fonttxt="", fontitle=""):
    """Create a text slide.
    bgfile: filename of the background picture
    txtfile: filename of the content
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    text = unicode(open(txtfile).read(), "UTF-8")
    # Use the complemetary color of the picture for the text
    avgcolor = cbColor.avgcolor(image)
    compcolor = cbColor.compcolor(avgcolor)
    draw = ImageDraw.Draw(image)
    if fontitle == "":
        fontitle = "fonts/{:03}.ttf".format(randint(1, 4))
    if fonttxt == "":
        fonttxt = "fonts/{:03}.ttf".format(randint(1, 4))
        if fonttxt == fontitle:
            # Retry once, if it's still the same, ignore it
            fonttxt = "fonts/{:03}.ttf".format(randint(1, 4))
    fontt = ImageFont.truetype(fontitle, 600, encoding="unic")
    fontx = ImageFont.truetype(fonttxt, 300, encoding="unic")
    sizet = draw.textsize(title, font=fontt)
    text = autowrap(text, 2661 - 2 * draw.textsize(text[0], font=fontx)[0] , draw, fontx)
    sizex = draw.textsize(text, font=fontx)
    leftt = (2661 - sizet[0]) // 2
    # Set margin to the width of a character
    leftx = draw.textsize(text[0], font=fontx)[0]
    top = (3072 - 2 * sizet[1] - sizex[1]) // 2
    draw.text((leftt, top), title, font=fontt, fill=compcolor)
    draw.text((leftx, top + 2 * sizet[1]), text, font=fontx, fill=compcolor)
    return image
