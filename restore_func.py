#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')



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

    restorefilelist(args.oldfolder, args.newfolder, args.filelist, args.originalpath)
