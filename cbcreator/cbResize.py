from PIL import Image, ImageDraw, ImageFont

# interface to PIL.Image.resize
def resize(src):
    """ Resize given picture to 78*90.
    src: filename of the file
    returns PIL.Image object of the resized picture."""
    with Image.open(src) as file:
        return file.resize((2948,3401))
