#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Model:
    # automaton description.
    initState = 0
    transitionList = []
    nextTransition = []
    idxAssum = 0
    maxLabelTransition = 0
    maxLabelState = 0

    # abstract method
    def run(self):
        pass
