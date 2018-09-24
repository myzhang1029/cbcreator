from __future__ import print_function
from sys import argv, exit, stderr
from getopt import gnu_getopt as getopt, GetoptError
import cbResize

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

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
\t-r:\tjust cut (or resize) the image, and exit
\t-s:\tresize the image to 78*90 when needed, the default behavior is cut the additional part
""");

def start():
    textfile = None
    resize = False
    try:
        opts, args = getopt(argv[1:], "b:t:x:o:shr")
    except GetoptError as err:
        eprint(str(err))
        printhelp()
        exit(1)
    for o, a in opts:
        if o == "-h":
            printhelp()
            exit(0)
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
        elif o == "-o":
            outputfn = a
        else:
            assert False, "unhandled option"
    if cut_only:
        try:
            cbResize.resize(backgroundfile).save(outputfn)
        except UnboundLocalError:
            eprint("You must supply a -o option and a -b option")
            exit(1)
        exit(0)

if __name__ == "__main__":
    start()
