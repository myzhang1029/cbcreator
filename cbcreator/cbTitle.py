from PIL import Image, ImageDraw, ImageFont
import cbResize

def create(bgfile, title):
    """Create a title slide.
    bgfile: filename of the background picture
    returns PIL.Image object of the created picture."""
    image = cbResize.resize(bgfile)
    draw = ImageDraw(image)
    pass
