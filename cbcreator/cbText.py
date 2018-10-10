from __future__ import division
from PIL import Image, ImageDraw, ImageFont
from random import randint
import cbResize
import cbColor

def autowrap(text, width, draw, font):
    """ Word-wrap text to a fixed width
    text: the text to be wraped
    width: the width of every line
    draw: pillow ImageDraw object
    font: the pillow ImageFont object to be used
    returns the wraped text"""
    lines = text.split('\n')
    if ''.join(lines) != text:
        # Already contains LFs
        wrapped = ""
        for line in lines:
            wrapped += autowrap(line, width, draw, font)
            wrapped += '\n'
        return wrapped
    initsz = draw.textsize(text, font=font)[0]
    txtlen = len(text)
    if txtlen == 0:
        return ""
    # shouldn't split a character into two
    wraploc = initsz / width # lines the text should be
    wraploc = round(txtlen / wraploc) # lenth of every line
    # leave some spare space for the round-off
    wraploc -= 1
    print(initsz, width, wraploc, txtlen)
    resultstr = ""
    for idx in range(0, txtlen):
        # insert a LF whenever the wraploc-th char is met
        if idx % wraploc == 0 and idx != 0:
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
    # load the font for the title and the text
    if fontitle == "":
        fontitle = "fonts/{:03}.ttf".format(randint(1, 4))
    fontt = ImageFont.truetype(fontitle, 600, encoding="unic")
    if fonttxt == "":
        fonttxt = "fonts/{:03}.ttf".format(randint(1, 4))
    fontx = ImageFont.truetype(fonttxt, 100, encoding="unic")
    # size tuple of the title
    sizet = draw.textsize(title, font=fontt)
    onechar = draw.textsize(title[0], font=fontx)[0]
    # don't ask what the 3 is, it just works
    text = autowrap(text, 2661 - 3 * onechar, draw, fontx)
    sizex = draw.textsize(text, font=fontx)
    leftt = (2661 - sizet[0]) // 2
    # Set margin to the width of a character
    leftx = (2661 - sizex[0]) // 2
    top = (3072 - sizet[1] - sizex[1] - onechar) // 2
    draw.text((leftt, top), title, font=fontt, fill=compcolor)
    draw.text((leftx, top + sizet[1] + onechar), text, font=fontx, fill=compcolor)
    return image
