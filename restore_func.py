#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}



def restorefilelist(oldfolder, newfolder, filelist, originalpath = None):
    import os
    import shutil

    if originalpath is None:
        originalpath = newfolder

    if oldfolder[-1] != '/':
        oldfolder = oldfolder + '/'
    if newfolder[-1] != '/':
        newfolder = newfolder + '/'
    if originalpath[-1] != '/':
        originalpath = originalpath + '/'

    with open(filelist, 'r', encoding = 'latin-1') as f:
        files = f.read().splitlines()

    for filename in files:
        oldfilename = filename.replace(originalpath, oldfolder)
        newfilename = filename.replace(originalpath, newfolder)

        # if not os.path.isdir(folder):
        #     os.makedirs(folder)

        # folder = os.path.dirname(newfilename)
        if os.path.isdir(oldfilename):
            try:
                os.makedirs(newfilename)
            except Exception:
                None
        else:
            shutil.copyfile(oldfilename, newfilename)


def restorefilelist_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("oldfolder")
    parser.add_argument("newfolder")
    parser.add_argument("filelist")
    parser.add_argument("--originalpath")
    
    args=parser.parse_args()
    #End argparse:}}}

    importattr(__projectdir__ / Path('restore_func.py'), 'restorefilelist')(args.oldfolder, args.newfolder, args.filelist, args.originalpath)
