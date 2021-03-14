# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:38:22 2021

@author: Rob
"""
import os
import filecmp #compare directories and files
import difflib #compare file contents
from datetime import datetime
from math import isclose
#import watchdog
import hashlib

def testing_stuff():
    d1 = 'D:\\Users\\Rob\\Documents\\python\\'
    d2 = r'F:\python'
    #d2 = d1
    d = filecmp.dircmp(d1,d2, ignore=filecmp.DEFAULT_IGNORES+['.js','.zip','.ipynb_checkpoints', '.spyproject', '.pylint*'])
    filecmp.DEFAULT_IGNORES
    d.report()
    d.report_full_closure()
    #filecmp.cmp(f1,f2,shallow=False) #typical for comparison of two files
    (same, diff, irreg) = filecmp.cmpfiles(d1,d2, d.common_files,shallow=False)#compare common files in 2 dirs
    d.left_only
    d.right_only
    d.common

def my_full_closure(d, top=True): # Report on d and subdirs recursively
    #put in a dict or similar instead of just printing
    stime = datetime.now().timestamp()
    bigdict = dict()
    bigdict[d.left+"-->"+d.right] = {'left':d.left_only, 'right':d.right_only,'commonf':d.common_files,'commondirs':d.common_dirs,'funny':d.common_funny}
    #d.report()
    for sd in d.subdirs.values():
        #print()
        bigdict.update(my_full_closure(sd, top=False) )#recurse
    etime = datetime.now().timestamp()
    if top: print(f"compared {len(bigdict)} dirs in {etime-stime} secs")
    return bigdict

import timeit

def test_my_full_closuer():       
    d1 = 'D:\\Users\\Rob\\Documents\\python\\'
    d2 = r'F:\python'
    #d2 = d1
    d = filecmp.dircmp(d1,d2, ignore=filecmp.DEFAULT_IGNORES+['.js','.zip','.ipynb_checkpoints', '.spyproject', '.pylint*'])

    full_cmp = my_full_closure(d)

    for k in full_cmp.keys():
        #print(f"k is {k}")
        (leftdir, rightdir) = k.split('-->')
        for f in full_cmp[k]['left']:#files to copy left to right
            print("->",os.path.join(leftdir,f), "copy to", os.path.join(rightdir,f))
        for f in full_cmp[k]['right']:#files to copy from right to left
            print("<-",os.path.join(rightdir,f), "copy to", os.path.join(leftdir,f))
        #for full_cmp[k]['commonf'] we need to use filecmp.cmpfiles
        (same, diff, irreg) = filecmp.cmpfiles(leftdir,rightdir, full_cmp[k]['commonf'],shallow=False)
        if len(diff) > 0:
            print(f"these files are common but might have been changed {k}")
            for cd in diff:
                print(cd)
                #check size
                #check mtimes
                #check hash
        if len(irreg) >0:
            print(f"these files were common but couldn't be compared {k} {diff}")
        #commondirs are covered by recursion
        #for funny we report
        if len(full_cmp[k]['funny']) > 0:
            print(f"these files were funny: {full_cmp[k]['funny']}")

def testing_dircmp_for_common():
    testdir= r'D:\Users\Rob\Documents\python\syncdirs\syncdirs-->F:\python\syncdirs\syncdirs'
    (leftdir, rightdir) = testdir.split('-->')
    lrcmp  = filecmp.dircmp(leftdir, rightdir)
    lrcmp.common_files, lrcmp.common, lrcmp.common_dirs, lrcmp.common_funny
    (same, diff, irreg) = filecmp.cmpfiles(leftdir,rightdir, lrcmp.common_files,shallow=False)#compare common files in 2 dirs
    #files on disk get msec chopped off so might not report the same timestamp
    # even when the files are identical
    
def testing_common_drilldown():
    s1 = hashlib.sha1(open(os.path.join(leftdir,diff[0]), 'rb').read())
    s1.hexdigest()
    #files could have diff timesamps but have the exact same contents
    # hash the files and compare the values to determine
    # only do this if size is the same but tiemstamp is different?
    #md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(), sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.
    os.path.getmtime(os.path.join(leftdir,diff[0])), os.path.getmtime(os.path.join(rightdir,diff[0]))
    datetime.fromtimestamp(os.path.getmtime(os.path.join(leftdir,diff[0]))), datetime.fromtimestamp(os.path.getmtime(os.path.join(rightdir,diff[0])))
    os.path.getsize(os.path.join(leftdir,diff[0])), os.path.getsize(os.path.join(rightdir,diff[0]))

def check_hashes(leftfile, rightfile, hasher=hashlib.md5()):
    """ check a hash of leftfile and rightfile to ensure they are the same
    - pass in the hashtype using the constructor 
    - then use update to add the data to the selected type?

    Parameters
    ----------
    leftfile : string for full file path
    rightfile : string for full file path

    Returns - boolean maybe?
    """
    lefthash = hasher.copy() #use the same hasthype for both
    righthash = hasher
    
    lefthash.update(leftfile.encode())#open(leftfile, 'rb').read())
    righthash.update(rightfile.encode())#open(rightfile, 'rb').read())
    return lefthash.hexdigest() == righthash.hexdigest()

def check_hashes_files(leftfile, rightfile, hasher=hashlib.md5()):
    """
    
    """
    lefts = open(leftfile, 'r').read()
    rights = open(rightfile, 'r').read()
    return check_hashes(lefts,rights, hasher)

def test_check_hashes():
    print(check_hashes('fred', 'fred'))#True
    print(check_hashes('fred', 'tom'))#False
    check_hashes_files(r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\syncdirs.py',r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\syncdirs.py')
    check_hashes_files(r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\misc.py',r'f:\python\syncdirs\syncdirs\misc.py')




def show_exp_as_float():
    print(f"def rel dif for isclose is {1e-9:.9f} abs dif is 0.0")


def fix_doublespace():
    os.chdir(r'syncdirs\syncdirs')
    
    with open(r'syncdirs.py','r') as f:
        s=f.read()
        
    s2=s.replace('\n\n','\n')
    print(s2)
    with open(r'syncdirs.py','w') as f:
       f.write(s2)


if __name__ == '__main__':
    print('main')