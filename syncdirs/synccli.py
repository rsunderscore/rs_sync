#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 21:28:41 2021

@author: rob
"""

from argparse import ArgumentParser

import utils as u

def main():
    print("in main")
    desc = """This program will compare two directories (sdir and ddir) and verify 
    whether they contain the same files and folders.
    """
    conflict_options = ['bigger', 'newer', 'smaller', 'older']
    a = ArgumentParser(description=desc)
    a.add_argument('sdir', action='store', default='.', help="(aka leftdir) a directory to compare")
    a.add_argument('ddir', action='store', help='(aka rightdir) a directory to compare')
    a.add_argument('--report_only', '-r', action='store_true', help="boolean: if specified then don't make any changes only report - default: False")
    #a.add_argument('--favor_newer', action='store_true', help="boolean: if specified new files will overwrite old when they exist in both places - default: False")
    a.add_argument('--conflict_handling', choices=conflict_options, default='newer', help = "what to when a file is in both locations")
        
    #args = a.parse_args(['one', 'two'])
    args = a.parse_args()
    favor_newer = True if args.conflict_handling == 'newer' else False
        

    print(f"comparing path {args.sdir} to {args.ddir} report_only is {args.report_only}")
    print(args)
    s = u.sync(args.sdir, args.ddir, args.report_only, favor_newer)
    print(s)
    
if __name__ == '__main__':
    main()