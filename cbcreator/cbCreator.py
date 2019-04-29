# cbcreator.py - main routines to render a class band slide
#
# Copyright 2018 Zhang Maiyun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, division
from sys import argv, exit, stdin, stdout, stderr, version_info
from os.path import realpath, dirname, isfile
from random import randint
from getopt import gnu_getopt as getopt, GetoptError
from PIL import Image, ImageDraw, ImageFont

__all__ = ['BandSlide', 'autowrap', 'avgcolor',
           'compcolor', 'eprint', 'getrc', 'start']

if version_info[0] == 3:
    def unicode(s, e):
        return s

    def isstr(s):
        return isinstance(s, (bytes, str))
else:
    range = xrange
    input = raw_input

    def isstr(s):
        return isinstance(s, basestring)
    systemunicode = unicode

    def unicode(s, e): return systemunicode(s, e) if s else s


def getrc(rcname):
    """ Get a program resource placed in cbcreator/resources.
    rcnane: The filename
    returns the full path to the file.
    """
    scriptpath = realpath(__file__)
    if isfile(scriptpath):
        scriptpath = dirname(scriptpath)
    rc = scriptpath + "/resources/" + rcname
    return rc


def avgcolor(imageobj):
    """ Get the average color of the PIL.Image object.
    imageobj: the image
    returns a RGB tuple.
    """
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
    r //= totalcount
    g //= totalcount
    b //= totalcount
    return (r, g, b)


def compcolor(color):
    """ Compute the complementary color of the given color.
    color: the color to be computed
    returns a RGB tuple.
    """
    return (255 - color[0], 255 - color[1], 255 - color[2])


def autowrap(text, width, draw, font):
    """ Word-wrap text to a fixed width
    text: the text to be wrapped
    width: the width of every line
    draw: pillow ImageDraw object
    font: the pillow ImageFont object to be used
    returns the wrapped text.
    """
    if not text:
        return ""
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
    wraploc = initsz / width  # lines the text should be
    wraploc = round(txtlen / wraploc)  # lenth of every line
    # leave some spare space for the round-off
    wraploc -= 1
    resultstr = ""
    for idx in range(0, txtlen):
        # insert a LF whenever the wraploc-th char is met
        if idx % wraploc == 0 and idx != 0:
            resultstr += '\n'
        resultstr += text[idx]
    return resultstr


class BandSlide(object):
    """ Class wrapper of a class band slide. """

    def __init__(self, bgfile):
        """ Create a class band slide object.
        bgfile: file name or file object of the background
        """
        self.im = Image.open(bgfile).resize((2661, 3072))
        self.title = None
        self.text = None
        self.pics = []
        self.titlefont = None
        self.titlesize = 600
        self.titlecolor = compcolor(avgcolor(self.im))
        self.textfont = None
        self.textsize = 100
        self.textcolor = compcolor(avgcolor(self.im))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """ Close all images. """
        try:
            self.im.close()
            self.im = None
            for pic in self.pics:
                pic.close()
        except:
            pass

    def addtitle(self, title):
        """ Add a title to the slide. """
        self.title = unicode(title, "UTF-8")

    def addtext(self, textfile):
        """ Add text to the slide. """
        if isstr(textfile):
            self.text = unicode(open(textfile).read(), "UTF-8")
        elif textfile is not None:
            self.text = unicode(textfile.read(), "UTF-8")
        else:
            pass  # None, nothing added

    def addpic(self, pics):
        """ Add picture to the slide.
        pics: path, file object, tuple or list
        """
        if not pics:
            return
        try:
            for pic in pics:
                if pic:  # Not empty or None
                    self.pics.append(Image.open(pic))
        except TypeError:
            self.pics.append(Image.open(pics))

    def set_title_attrib(self, **kwargs):
        """ Set attributes of the title.
        kwargs: attributes
            possible keys:
                font: full path of the font file
                color: color specified in RGB tuple
                size: font size in pixels
            Note that you should always specify size before font.
        """
        for attrib in kwargs:
            if attrib == "font":
                self.titlefont = ImageFont.truetype(
                    kwargs[attrib],
                    self.titlesize,
                    encoding="unic")
            elif attrib == "color":
                self.titlecolor = kwargs[attrib]
            elif attrib == "size":
                self.titlesize = int(kwargs[attrib])
            else:
                raise ValueError("Unexpected key {}".format(attrib))

    def set_text_attrib(self, **kwargs):
        """ Set attributes of the text.
        kwargs: attributes
            possible keys:
                font: full path of the font file
                color: color specified in RGB tuple
                size: font size in pixels
            Note that you should always specify size before font.
        """
        for attrib in kwargs:
            if attrib == "font":
                self.textfont = ImageFont.truetype(
                    kwargs[attrib],
                    self.textsize,
                    encoding="unic")
            elif attrib == "color":
                self.textcolor = kwargs[attrib]
            elif attrib == "size":
                self.textsize = int(kwargs[attrib])
            else:
                raise ValueError("Unexpected key {}".format(attrib))

    def save(self, output):
        if self.titlefont == None:
            fontfile = "fonts/{:03}.ttf".format(randint(1, 4))
            fontfile = getrc(fontfile)
            self.titlefont = ImageFont.truetype(
                fontfile, self.titlesize, encoding="unic")
        """ Save the slide to a file. """
        if self.textfont == None:
            fontfile = "fonts/{:03}.ttf".format(randint(1, 4))
            fontfile = getrc(fontfile)
            self.textfont = ImageFont.truetype(
                fontfile, self.textsize, encoding="unic")
        # Only create the ImageDraw object if we aren't just resizing
        if self.title or self.text or self.pics:
            draw = ImageDraw.Draw(self.im)
            if not self.title:
                self.title = ""
            # size tuple of the title
            sizet = draw.textsize(self.title, font=self.titlefont)
            onechar = draw.textsize("a", font=self.textfont)[0]
            # don't ask what the 3 is, it just works
            self.text = autowrap(self.text, 2661 - 3 *
                                 onechar, draw, self.textfont)
            sizex = draw.textsize(self.text, font=self.textfont)
            leftt = (2661 - sizet[0]) // 2
            # Set margin to the width of a character
            leftx = (2661 - sizex[0]) // 2
            top = (3072 - sizet[1] - sizex[1] - onechar) // 2
            draw.text((leftt, top), self.title,
                      font=self.titlefont, fill=self.titlecolor)
            draw.text((leftx, top + sizet[1] + onechar),
                      self.text, font=self.textfont, fill=self.textcolor)
            # # TODO: Render the slide to self.im
            # #       Use https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=overlay#PIL.Image.Image.alpha_composite
        self.im.save(output)

    
def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def parsecmd():
    def printhelp(): return eprint("""
Usage:
\tcbcreator -b bgpic -t title [-x text] -o output [-s] | -h | -r
Required options:
\t-b bgpic:\tspecify the background, full path or relative
\t-o output:\tspecify the output file
Optional options:
\t-t title:\tspecify the title
\t-x text:\tfile of the text on the slide, nothing for a title slide
\t-a pic:\toverlay pictures on the slide
""")

    bgfile = None
    title = None
    textfile = None
    outputfile = None
    overlay = []
    try:
        opts, args = getopt(argv[1:], "b:t:x:o:hr")
    except GetoptError as err:
        printhelp()
        eprint(str(err))
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
        elif o == "-o":
            outputfile = a
        elif o == "-a":
            overlay.append(a)
        else:
            assert False, "unhandled option"
    if bgfile == None:
        printhelp()
        eprint("Error: You must supply option -b")
        exit(1)
    if outputfile == None:
        printhelp()
        eprint("Error: You must supply option -o")
        exit(1)
    # Read from stdin/write to stdout
    if bgfile == "-":
        bgfile = stdin
    if outputfile == "-":
        outputfile = stdout
    slide = BandSlide(bgfile)
    slide.addtitle(title)
    slide.addtext(textfile)
    slide.addpic(overlay)
    slide.save(outputfile)

def interactive():
    currentin = None
    overlay = []
    while True:
        bgfile = input("The file to be used as the background: ")
        if bgfile:
            break
        eprint("Don't left this field blank!")
    title = input("The title for the page: ")
    textfile = input("The text file to use: ")
    while True:
        outputfile = input("Where to output: ")
        if outputfile:
            break
        eprint("Don't left this field blank!")
    while True:
        currentin = input("Pictures to lay on(left blank to stop): ")
        if currentin:
            overlay.append(currentin)
        else:
            break
    slide = BandSlide(bgfile)
    slide.addtitle(title)
    slide.addtext(textfile)
    slide.addpic(overlay)
    slide.save(outputfile)


def start():
    try:
        _=argv[1]
    except IndexError:
        # No command line provided
        interactive()
    parsecmd()

if __name__ == "__main__":
    start()
