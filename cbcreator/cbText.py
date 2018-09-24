from PIL import Image, ImageDraw, ImageText
import cbResize

def create(bgfile, txtfie, title):
    """Create a text slide.
    bgfile: filename of the background picture
    txtfile: filename of the content
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    draw = ImageDraw(image)
    pass
