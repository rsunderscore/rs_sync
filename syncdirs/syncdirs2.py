# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:12:48 2016
@author: Robert
"""
# -*- coding: utf-8 -*-
#!C:\Program Files\Anaconda3\python.exe
"""
Created on Mon Oct 31 10:40:27 2016
#replacement for synctoy
@author: NBKXO1N
"""
from glob import glob
from datetime import datetime as dt2
from dateutil.parser import parse
import os, sys, shutil
 
def main():
    print(sys.argv[0])
   
    sourcdir=r"c:\users\nbkxo1n\documents\my sas files"
    spath=os.path.split(sourcdir)
    destdir=os.path.join(r"h:\documents",spath[-1])
    print(destdir)
    #handle CLI params
    if(len(sys.argv)>1):
        if(len(sys.argv[1])>0):
            sourcdir=sys.argv[1]
        if(len(sys.argv[2])>0):#need better handling for dest in function
            destdir=sys.argv[2]
    else: print("no cli args")
    #sync directories
    copynew(sourcdir, destdir)
 
#d_src={x:(dt2.fromtimestamp(os.stat(x).st_mtime), os.stat(x).st_size) for x in \
#       glob(sourcdir+"\\*")}
#d_dst={x:(dt2.fromtimestamp(os.stat(x).st_mtime), os.stat(x).st_size) for x in \
#       glob(destdir+"\\*")} #dict for shared folder hangs need to state one file at a time
def copynew(strpath, destdir):#need an arge for the base destindation directory
    """replicate the fs tree of strpath in destdir'
        if srcpath file is newer or doesn't exist then copy it
        - bug where mutliple runs are required to get everything synced
        - picks up a new file with each run

    """
    d_src = glob(strpath+"\\*")
    depth=1#not sure how to track recursion depth
    for curpth in d_src:
        if os.path.basename(curpth)[0] == '_': continue #skip files/dirs that start with underscore e.g. __pycache__
        #if the name is a directory then recurse
        dstpth = destdir+"\\"+os.path.split(curpth)[1]
        #print("{} vs {}".format(curpth, dstpth))
        if not(os.path.isfile(dstpth) or os.path.isdir(dstpth)):
            if(os.path.isdir(curpth) ):
                print("creating directory {}".format(dstpth))
                os.mkdir(dstpth)#cant copy2 a directory
                copynew(curpth, dstpth)
            else:
                print("{} does not exist...copying".format(dstpth))#check dst pth for the file
                #if the file doesn't exist in the dest then copy it
                shutil.copy2(curpth,dstpth)
                #if the file doesn't exist then copy it
            return#is this needed?
        elif os.path.isdir(curpth):#recursive call to look at subpaths - need to update destdir as well
            #print("{} is a  directory".format(curpth))
            #print("*"*20+ "subdir {}".format(curpth)+"*"*20)
            copynew(curpth,dstpth)
        else:#file is a file that needs to be checked
            #if the file is newer or the file is  a different size - copy it to the dest path
            #print("{} is a file: mtime={} size={}bytes".format(curpth,os.stat(curpth).st_mtime,os.stat(curpth).st_size))
            #if the file is newer than the one in dest then copy it
           if(os.path.getmtime(curpth) > os.path.getmtime(dstpth)):#if file is newer - may need to check size as well
                print("*** {} is newer than {}... syncing".format(curpth,dstpth))
                shutil.copy2(curpth,dstpth)
    #else do nothing
    print("done with {} syncing new files to {} ".format(strpath, destdir))
    print("*"*25)
    return
   
 
if __name__ == "main": main()
else: print("not main")