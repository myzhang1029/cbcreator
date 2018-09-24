from PIL import Image
# interface to PIL.Image.resize
def resize(src):
    """ Resize given picture to 78*90.
    src: filename of the file
    returns PIL.Image object of the resized picture."""
    return Image.open(src).resize((2948,3401))
