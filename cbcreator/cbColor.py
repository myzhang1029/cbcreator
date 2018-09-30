from PIL import Image

def avgcolor(imageobj):
    """ Get the average color of the PIL.Image object
    imageobj: the image
    returns a RGB tuple."""
    r = 0
    g = 0
    b = 0
    totalcount = 0
    colors = 256
    arr = None
    while True:
        arr = imageobj.getcolors(colors)
        if arr == None:
            colors *= 2
        else:
            break
    for tup in arr:
        r += tup[0] * tup[1][0]
        g += tup[0] * tup[1][1]
        b += tup[0] * tup[1][2]
        totalcount += tup[0]
    r /= totalcount
    g /= totalcount
    b /= totalcount
    return (r, g, b)

def compcolor(color):
    """ Compute the complementary color of the goven color
    color: the color to be computed
    returns a RGB tuple."""
    return (255 - color[0], 255 - color[1], 255 - color[2])
