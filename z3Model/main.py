#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from kDiagModel import ModelZ3kDiag

# the automata.
assert(len(sys.argv) == 2)
z3Model = ModelZ3kDiag(sys.argv[1])
z3Model.printAutomatonInfo()
z3Model.run()
