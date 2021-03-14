# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 19:02:11 2020

@author: Robert
"""
import os
from argparse import ArgumentParser
from shutil import copy2
from watchdog.utils import dirsnapshot

def usewd():
    s = dirsnapshot.DirectorySnapshot('.')
    n = dirsnapshot.DirectorySnapshot(r'\\HPTM2\Users\Robert\Documents\Python')
    #uses the full path instead of assuming provided is root for both
    changes = dirsnapshot.DirectorySnapshotDiff(s, n, ignore_device=True)
    #ignore dunder locations e.g. __pycache__

def main():
    a = ArgumentParser()
    a.add_argument('sdir', action='store', default='.')
    a.add_argument('ddir', action='store')
    #args = a.parse_args(['one', 'two'])
    args = a.parse_args()
    print(f"comparing path {args.sdir} to {args.ddir}")
    #TODO handle cmdline
    cmp_dirs('.')
    
def cmp_dirs(src,dst, docopy=False):
    #make sure one is not a subdir of the other
    #flags: direction, update, 
    #%%
    for (cur, dirs, files) in os.walk(src):
        #print(cur, dirs, files)
        if os.path.basename(cur)[0] == '_':
            print(f"skipping cur {cur}")
            continue
        for x in dirs:
            fullpath = os.path.join(cur,x)

            if os.path.basename(fullpath)[0] == '_': 
                print(f"skipping {fullpath}")
                continue
            print(f"\n***looping through {fullpath} | ", os.path.basename(fullpath)[0])
            dstname = fullpath.replace(src,dst, 1)#replace only first
            if not os.path.exists(dstname):
                print(f"{dstname} doesn't exist - need to create")
            #if dir doesn't exist copy it
            #if dir does exist recurse
        for f in files:
            if os.path.basename(f)[0] == '_': continue
            print("f", end="")
            #if file doesn't exist copy it
            #if file does exist compare the dates
            #copy the newer file
        print(f"\t\t--> done with {cur}")

if __name__ == '__main__': main()