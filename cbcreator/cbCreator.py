from __future__ import print_function
from sys import argv, exit, stderr
from getopt import gnu_getopt as getopt, GetoptError
import cbResize
import cbTitle
import cbText

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
\t-x text:\tfile of the text on the slide, nothing for a title slide
\t-r:\tjust cut (or resize) the image, and exit
""");

def start():
    textfile = None
    resize = False
    bgfile = None
    optputfile = None
    title = None
    try:
        opts, args = getopt(argv[1:], "b:t:x:o:hr")
    except GetoptError as err:
        eprint(str(err))
        printhelp()
        exit(1)
    for o, a in opts:
        if o == "-h":
            printhelp()
            exit(0)
        elif o == "-b":
            bgfile = a
        elif o == "-t":
            title = a
        elif o == "-x":
            textfile = a
        elif o == "-r":
            cut_only = True
        elif o == "-o":
            outputfile = a
        else:
            assert False, "unhandled option"
    if bgfile == None:
        eprint("You must supply option -b")
        exit(1)
    if outputfile == None:
        eprint("You must supply option -o")
        exit(1)
    if cut_only:
        cbResize.resize(bgfile).save(outputfile)
        exit(0)
    if title == None:
        eprint("Your must supply option -t if option -r not supplied")
        exit(1)
    if textfile == None:
        cbTitle.create(bgfile, title).save(outputfile)
    else:
        cbText.create(bgfile, textfile, title).save(outputfile)
    exit(0)

if __name__ == "__main__":
    start()
