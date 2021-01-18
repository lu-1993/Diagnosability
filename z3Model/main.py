#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
from kDiagToZ3gModel import KDiagToZ3Model

# Instantiate the options parser
parser = argparse.ArgumentParser(description='Diagnosis tool')
parser.add_argument('file', help='The input file path.')
parser.add_argument('--method', required=True, choices=['kDiag', 'lDiag'],
                    help='Which kind of dignosis process we want to use')
parser.add_argument('--symmetry', default=False, action='store_true', help='Is the symmetry breaking constraints have been added?')
parser.add_argument('--recar', default=False, action='store_true', help='Is the RECAR mode activated?')
args = parser.parse_args()

if args.method == 'kDiag':
    print("[MAIN]", "K diagnosis process")
    z3Model = KDiagToZ3Model(args.file)
    z3Model.displayInfo()
    z3Model.run()
else:
    print("[MAIN]", "Loop diagnosis process")