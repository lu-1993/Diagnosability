#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Model(ABC):
    # automaton description.
    initState = 0
    transitionList = []
    nextTransition = []
    idxAssum = 0
    maxLabelTransition = 0
    maxLabelState = 0

    def __init__(self):
        pass

    def printAutomatonInfo(self):
        """
        Print information about the given automaton
        """
        print("Information ...")
        print("automata:")
        for i in range(len(self.transitionList)):
            print(i, ":", self.transitionList[i])

        print("initial state:", self.initState)

        print("next transition:")
        for i in range(len(self.nextTransition)):
            print(i, ':', self.nextTransition[i])


    # abstract method
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def displayInfo(self):
        pass

    @abstractmethod
    def printModel(self, model):
        pass

    @abstractmethod
    def checkModel(self, model):
        pass
