#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from parser import Parser

class Model(ABC):
    # automaton description.
    initState = 0
    transitionList = []
    nextTransition = []
    idxAssum = 0
    maxLabelTransition = 0
    maxLabelState = 0

    @abstractmethod
    def __init__(self, nameFile):
        """
        Constructor.

        :param nameFile: the file where is stored the automaton with the parameters (i.e. k and B).
        :type nameFile str
        """
        print("[MODEL] Parsing starts ...")
        # parse the file and store the automaton
        p = Parser()
        self.initState, self.transitionList, self.BOUND, self.K = p.parse(nameFile)
        print("[MODEL] k =", self.K)
        print("[MODEL] B =", self.BOUND)

        # we add a transition, that is the nop transition, in position 0 in the transitionList
        self.transitionList.insert(0, [-1,-1,0])

        self.nextTransition = [[self.NOP_TRANSITION] for i in range(len(self.transitionList))] # they can all do nop
        for i in range(len(self.transitionList)):
            # fix the limit and store the id of the observable transitions.
            if self.transitionList[i][2] > self.maxLabelTransition:
                self.maxLabelTransition = self.transitionList[i][2]

            if self.transitionList[i][0] > self.maxLabelState:
                self.maxLabelState = self.transitionList[i][0]

            if self.transitionList[i][1] > self.maxLabelState:
                self.maxLabelState = self.transitionList[i][1]

            # for a transition t, collect the list of possible next transition that can be executed after t.
            for j in range(len(self.transitionList)):
                if (self.transitionList[i][1] == self.transitionList[j][0]):
                    self.nextTransition[i].append(j)

        # we add a transition to start the two path identically.
        self.maxLabelState += 1
        self.transitionList.append([self.maxLabelState, self.initState, 2])
        self.nextTransition.append([self.NOP_TRANSITION])
        self.nextTransition[-1] += [idx for idx in range(len(self.transitionList)) if self.transitionList[idx][0] == self.initState]

        print("[MODEL] Parsing done.")


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

    @abstractmethod
    def printModel(self, model):
        pass

    @abstractmethod
    def incVariableList(self):
        pass

    @abstractmethod
    def incBound(self):
        pass

    @abstractmethod
    def addConstraintOnIdTransition(self, pos):
        pass
