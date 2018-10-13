from os.path import realpath, dirname, isfile

def getrc(rcname):
    """ Get a program resource placed in cbcreator/resources
    rcnane: The filename
    returns the full path to the file. """
    scriptpath = realpath(__file__)
    if isfile(scriptpath):
        scriptpath = dirname(scriptpath)
    rc = scriptpath + "/resources/" + rcname
    return rc
