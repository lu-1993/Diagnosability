#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
from kDiagCegarZ3gModel import KDiagCegarZ3Model

# Instantiate the options parser
parser = argparse.ArgumentParser(description='Diagnosis tool')
parser.add_argument('file', help='The input file path.')
parser.add_argument('--method', required=True, choices=['kDiag', 'lDiag'],
                    help='Which kind of dignosis process we want to use')
parser.add_argument('--symmetry', default=False, action='store_true', help='Is the symmetry breaking constraints have been added?')
parser.add_argument('--recar', default=False, action='store_true', help='Is the RECAR mode activated?')
parser.add_argument('-k', default=10, help='The allowed number of transitions after the fault.')
parser.add_argument('-B', default=10, help='The initial value for the bound.')
args = parser.parse_args()

assert args.recar == False

if args.method == 'kDiag':
    print("[RUN]", "K diagnosis process")
    print("[RUN] k =", args.k)
    print("[RUN] B =", args.B)

    z3Model = KDiagCegarZ3Model(args.file)
    z3Model.displayInfo()
    z3Model.run()
else:
    print("[RUN]", "Loop diagnosis process")
    print("[RUN] B =", args.B)
