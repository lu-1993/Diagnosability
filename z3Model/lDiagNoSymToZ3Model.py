#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from z3 import *
from z3Model import Z3Model

# Here are some suppositions:
# The NOP operation is represented by the ID 0
# The faulty transition is labelled with 1
# A non observable transition is labelled with 2

class LDiagNoSymToZ3Model (Z3Model):
    # z3 variables.
    cptFaultOccursByThePast = [ Int("cptFaultOccurs_1") ]
    delta = Int("delta")

    # parameter
    BOUND = 0

    # 'constants'
    NOP = 0
    FAULT = 1
    NO_OBS = 2
    NOP_TRANSITION = 0

    def __init__(self, nameFile):
        """
        Constructor.

        :param nameFile: where is stored the automaton
        :type nameFile: str
        """
        self.symActicated = False
        super().__init__(nameFile)

        # constraint on the first transition: cannot be nop by construction of possibleInitialTransition.
        self.s.add(self.faultyPath[0] == len(self.transitionList) - 1)
        self.s.add(self.normalPath[0] == len(self.transitionList) - 1)
        self.s.add(self.faultyPath[0] == self.lastlyActiveFaultyPath[0])
        self.s.add(self.normalPath[0] == self.lastlyActiveNormalPath[0])

        self.s.add(self.idTransitionNormalPath[0] != self.FAULT)
        self.s.add(self.nopFaultyPath[0] == False)
        self.s.add(self.nopNormalPath[0] == False)
        self.s.add(self.faultOccursByThePast[0] == (self.idTransitionFaultyPath[0] == self.FAULT))
        self.s.add(self.cptFaultOccursByThePast[0] == self.faultOccursByThePast[0])

        self.addConstraintOnIdTransition(0)


    def addConstraintOnIdTransition(self, pos):
        """
        Add the constraint that fix the id of the transition pos in both
        idTransitionFaultyPath and idTransitionNormalPath.

        :param pos: the position of the operation we consider.
        :type pos: int
        """
        super().addConstraintOnIdTransition(pos)



    def incVariableList(self):
        """
        Increment all the list with one new z3 variable.
        """
        super().incVariableList()

        # we increment the bound for the remaining variables.
        idx = len(self.cptFaultOccursByThePast) + 1
        self.cptFaultOccursByThePast.append(Int("cptFaultOccurs_" + str(idx)))
        self.checkSynchro.append(Bool("checkSynchro_" + str(idx)))


    def incBound(self):
        """
        Extend the bound allowing a new transition.
        """
        # increment the bound for the local variables.
        self.incVariableList()

        # increment the bound for the parent.
        super().incBound()

        # get the last variable.
        idx = len(self.faultyPath) - 1
        assert(idx > 0)

        # we add the constraints that specify the id of the transition
        self.addConstraintOnIdTransition(idx)


    def displayInfo(self):
        self.printAutomatonInfo()
        print("[L DIAG] BOUND:", self.BOUND)
        print("[L DIAG] Symmetry activated:", self.symActicated)


    def checkModel(self, model):
        """
        [DEBUG FUNCTION]
        Check out if the given model satisfies basic property s.t. transitions
        follow a valid scheme, the id are correct, ...

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        # TODO


    def printModel(self, model):
        """
        Print the model. That means information about the z3 variables and a output formal
        that can be considered for the checker.

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        super().printModel(model)


    def run(self):
        """
        Run the main program.
        """
        cpt = 1
        while cpt < (self.BOUND):
            cpt += 1
            self.incBound()        

        res = self.s.check()
        if res == sat:
            m = self.s.model()
            self.checkModel(m)
            self.printModel(m)
            return
        else:
            print("The problem is UNSAT")
