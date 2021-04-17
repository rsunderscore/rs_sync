# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:38:22 2021

@author: Rob
#replaced all prints with generic sring funcs in sync func
"""

import os, hashlib
from shutil import copy2, copytree
#from distutils.dir_utils import copytree #alternative
import filecmp #compare directories and files
#import difflib #compare file contents
from datetime import datetime
#from math import isclose
#import watchdog
#import timeit

def testing_stuff():
    #d1 = 'D:\\Users\\Rob\\Documents\\python\\'
    d1 = '/home/rob/Documents/python/'
    d2 = '/home/rob/Documents/Python/'
    #d2 = r'F:\python'
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

def setup_for_test_sync():
    from shutil import copytree, rmtree
    copytree('/home/rob/Documents/python', '/tmp/python')
    os.remove('/tmp/python/pyaudio_test.py')
    import syncdirs.utils as u
    s=u.sync('/home/rob/Documents/python', '/tmp/python', report_only=True)
    print(s)
    
def sync(dir1, dir2, report_only=True, favornewer=True):
    """compare dir1 and dir2 and ensure files and directories are the same
    report_only: if True then just report what would be done - 
    favornewer: what do do when the files are on both sides but seem to be the same(default: True)

    """
    #run my full closure
    #for every pair (dict keys)
    #copy left files to right
    #copy right files to left
    #for same files look at modified date and size and hash
        # if has is the same then ignore
        # if hash differs - copy newer file to folder of older file (overwrite)
    #create folders???
    d = filecmp.dircmp(dir1, dir2, ignore=filecmp.DEFAULT_IGNORES+['.js','.zip','.ipynb_checkpoints', '.spyproject', '.pylint*'])
    full_cmp = my_full_closure(d)
    #need to change print statemetns to generate output as string
    s = ""
    for k in full_cmp.keys():
        #s+=f"k is {k}\n"
        (leftdir, rightdir) = k.split('-->')
        for f in full_cmp[k]['left']:#files to copy left to right
            isdir = 'folder' if os.path.isdir(os.path.join(leftdir, f)) else 'file'
            s+=f"{isdir}->"+os.path.join(leftdir,f, "copy to", os.path.join(rightdir,f))+"\n"
            if not report_only and isdir =='file':
                copy2(os.path.join(leftdir,f),os.path.join(rightdir,f))
            elif not report_only and isdir=='folder':
                copytree(os.path.join(leftdir, f), os.path.join(rightdir,f))
        for f in full_cmp[k]['right']:#files to copy from right to left
            isdir = 'folder' if os.path.isdir(os.path.join(rightdir, f)) else 'file'
            s+=f"{isdir}<-"+ os.path.join(rightdir,f, "copy to", os.path.join(leftdir,f))+ "\n"
            if not report_only and isdir=='file': 
                copy2(os.path.join(rightdir,f),os.path.join(leftdir,f))
            elif not report_only and isdir=='folder':
                copytree(os.path.join(rightdir, f), os.path.join(leftdir,f))
        #for full_cmp[k]['commonf'] we need to use filecmp.cmpfiles
        #more granular checks for when the stat file the files happens to be the same
        (same, diff, irreg) = filecmp.cmpfiles(leftdir,rightdir, full_cmp[k]['commonf'],shallow=False)
        if len(diff) > 0:
            s+=f"these files are common but might have been changed {k} => {diff}\n"
            for cd in diff:
                #s+=cd
                #check hash
                torf = check_hashes_files(os.path.join(leftdir, cd), os.path.join(rightdir, cd))
                s+=f"hash compare for {cd} was {torf}\n"
                if not torf:
                    lmtime = os.path.getmtime(os.path.join(leftdir, cd))
                    rmtime = os.path.getmtime(os.path.join(rightdir, cd))
                    newerside = 'left' if lmtime > rmtime else 'right'
                    if not report_only and favornewer:
                        if lmtime > rmtime:
                            s+="copying left to right\n"
                            copy2(os.path.join(leftdir, cd), os.path.join(rightdir, cd))
                        else:
                            s+="copying right to left\n"
                            copy2(os.path.join(rightdir, cd), os.path.join(leftdir, cd))
                    s+=f"{newerside} is newer: left = {datetime.fromtimestamp(lmtime)}; right={datetime.fromtimestamp(rmtime)}\n"
                    lsize = os.path.getsize(os.path.join(leftdir, cd))
                    rsize = os.path.getsize(os.path.join(rightdir, cd))
                    biggerside = 'left' if lsize > rsize else 'right'
                    #annoyed
                    s+=f"{biggerside} is bigger: left={lsize}, right={rsize}\n"
            for sf in same:
                #check hash
                torf = check_hashes_files(os.path.join(leftdir, sf), os.path.join(rightdir, sf))
                if not torf: #file hashes not 
                    s+=f"{sf} file was in same list {leftdir} and {rightdir} but hashes are not equal\n"
                    #s+=f"hash compare for {sf} was {torf}\n"
                #check size
                #check mtimes
        if len(irreg) >0:
            s+=f"these files were common but couldn't be compared {k} {diff}\n"
        #commondirs are covered by recursion
        #for funny we report
        if len(full_cmp[k]['funny']) > 0:
            s+=f"these files were funny: {full_cmp[k]['funny']}\n"
    return s

def test_sync():
    from syncdirs import misc as m
    rightdir = '/media/rob/8B22-3665/python'
    leftdir = '/home/rob/Documents/python'
    m.sync(leftdir, rightdir, report_only=False)

def testing_dircmp_for_common():
    testdir= r'D:\Users\Rob\Documents\python\syncdirs\syncdirs-->F:\python\syncdirs\syncdirs'
    (leftdir, rightdir) = testdir.split('-->')
    lrcmp  = filecmp.dircmp(leftdir, rightdir)
    lrcmp.common_files, lrcmp.common, lrcmp.common_dirs, lrcmp.common_funny
    (same, diff, irreg) = filecmp.cmpfiles(leftdir,rightdir, lrcmp.common_files,shallow=False)#compare common files in 2 dirs
    same, diff, irreg
    #files on disk get msec chopped off so might not report the same timestamp
    # even when the files are identical
    
def testing_common_drilldown(leftdir, rightdir, same, diff, irreg):
    #files could have diff timesamps but have the exact same contents
    # hash the files and compare the values to determine
    # only do this if size is the same but tiemstamp is different?
    #md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(), sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.
    s1 = hashlib.sha1(open(os.path.join(leftdir,same[0]), 'rb').read())
    s2 = hashlib.sha1(open(os.path.join(rightdir,same[0]), 'rb').read())
    print(s1.hexdigest(), s2.hexdigest(), s1.hexdigest() == s2.hexdigest())

    l = os.path.getmtime(os.path.join(leftdir,same[0]))
    r = os.path.getmtime(os.path.join(rightdir,same[0]))
    print(f"{l} == {r} is {l==r}")
    datetime.fromtimestamp(os.path.getmtime(os.path.join(leftdir,same[0]))), datetime.fromtimestamp(os.path.getmtime(os.path.join(rightdir,same[0])))
    os.path.getsize(os.path.join(leftdir,same[0])), os.path.getsize(os.path.join(rightdir,same[0]))

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
    
    #expects string in binary so use encode if that isn't the case
    lefthash.update(leftfile)#open(leftfile, 'rb').read())
    righthash.update(rightfile)#open(rightfile, 'rb').read())
    return lefthash.hexdigest() == righthash.hexdigest()

def try_open(fname):
    #can we circumvent all of this just be opening in binary by default
    def open_normal(fname):
        return open(fname, 'r').read()
    def open_win(fname):
        return open(fname, 'r', encoding='cp1252').read()
    def open_binary(fname): #this should work if nothing else does
        return open(fname, 'rb').read()
    openoptions = {'normal':open_normal, 
                        'win': open_win, 
                        'binary': open_binary}
    for k in openoptions.keys():
        try:
            f=openoptions[k](fname)
            print(f"open worked using {k}")
            return f #if something works then leave
        except Exception as e:
            print(f"{k} open and read failed - trying something else")
            f=None
            raise(e)

def test_badfiles():

    #need to somehow loop through file open options until one works???
    badfile1 = '/home/rob/Documents/python/spanish/spshelf.dat'
    badfile2 = '/home/rob/Documents/python/spanish/irrlist.txt'

    f = try_open(badfile2)
    f = try_open(badfile1)
        
    hasher=hashlib.md5()
    hasher.update(f)
    hasher.hexdigest()

def check_hashes_files(leftfile, rightfile, hasher=hashlib.md5()):
    """
    Since hashing requires a string - read the files 
    """
    ### BUG: this gets tripped up on files with different encoding
    # can try to open using different methods or just open everything in binary
    try:
        lefts = open(leftfile, 'rb').read()
        rights = open(rightfile, 'rb').read()
    except UnicodeDecodeError as e:
        print(e, leftfile, rightfile)
        return None
    return check_hashes(lefts,rights, hasher)

def test_check_hashes():
    print(check_hashes('fred', 'fred'))#True
    print(check_hashes('fred', 'tom'))#False
    check_hashes_files(r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\syncdirs.py',r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\syncdirs.py')
    check_hashes_files(r'D:\Users\Rob\Documents\python\syncdirs\syncdirs\misc.py',r'f:\python\syncdirs\syncdirs\misc.py')
    #print(check_hashes_files(leftdir, rightdir))


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


