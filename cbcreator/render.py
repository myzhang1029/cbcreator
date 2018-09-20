from PIL import Image, ImageDraw, ImageFont
from sys import argv, exit, stderr
from getopt import gnu_getopt as getopt, GetoptError
from __future__ import print_function

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def printhelp():
    eprint("""
Usage:
\tcbcreator -b bgpic -t title [-x text] -o output [-s] | -h | -r
Required options:
\t-b bgpic:\tspecify the background, full path or relative
\t-t title:\tspecify the title
\t-o output:\tspecify the output file
Optional options:
\t-x text:\tthe text on the slide, no for a title slide
\t-r:\tjust cut the image
\t-s:\tresize the image to 78*90 when needed, the default behavior is cut the additional part
""");

def start():
    textfile = None
    resize = False
    try:
        opts. args = getopt(sys.argv[1:], "b:t:x:o:shr")
    except GetoptError as err:
        eprint(str(err))
        printhelp()
        exit(1)
    for o, a in opts:
        if o == "-h":
            printhelp()
            exit(1)
        elif o == "-b":
            backgroundfile = a
        elif o == "-t":
            title = a
        elif o == "-x":
            textfile = a
        elif o == "-s":
            resize = True
        elif o == "-r":
            cut_only = True
        else:
            assert False, "unhandled option"
    pass

if __name__ == "__main__":
    start()

