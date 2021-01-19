#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from z3 import *
from z3Model import Z3Model

# Here are some suppositions:
# The NOP operation is represented by the ID 0
# The faulty transition is labelled with 1
# A non observable transition is labelled with 2

class KDiagToZ3Model (Z3Model):
    # z3 variables.
    cptFaultOccursByThePast = [ Int("cptFaultOccurs_1") ]
    delta = Int("delta")

    # parameter
    BOUND = 0
    K = 0

    # 'constants'
    NOP = 0
    FAULT = 1
    NO_OBS = 2
    NOP_TRANSITION = 0

    def __init__(self, nameFile, symActicated):
        """
        Constructor.

        :param nameFile: where is stored the automaton
        :type nameFile: str
        :param symActicated: is the symmetry mode activated
        :type symActicated: bool
        """
        super().__init__(nameFile, symActicated)

        # constraint on the first transition: cannot be nop by construction of possibleInitialTransition.                
        self.s.add(self.delta == self.BOUND - self.K - 1)
        self.s.add(Implies(self.delta <= 0, self.faultOccursByThePast[0]))
        self.s.add(self.K >= 0)
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

        # count since when the first fault occurs
        self.s.add(Or(self.cptFaultOccursByThePast[pos] - 1 > self.K, Not(self.checkSynchro[pos]), self.idTransitionFaultyPath[pos] == self.idTransitionNormalPath[pos]))


    def incVariableList(self):
        """
        Increment all the list with one new z3 variable.
        """
        super().incVariableList()

        # we increment the bound for the remaining variables.
        idx = len(self.cptFaultOccursByThePast) + 1
        self.cptFaultOccursByThePast.append(Int("cptFaultOccurs_" + str(idx)))


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

        # we have a fault soon enough.
        self.s.add(Implies(self.delta <= idx, self.faultOccursByThePast[idx]))

        # set the counter since when the fault occurs.
        self.s.add(self.cptFaultOccursByThePast[idx] == self.cptFaultOccursByThePast[idx-1] + (And(self.faultyPath[idx] != self.NOP_TRANSITION, self.faultOccursByThePast[idx])))


    def displayInfo(self):
        self.printAutomatonInfo()
        print("[K DIAG] BOUND:", self.BOUND)
        print("[K DIAG] K:", self.K)
        print("[K DIAG] Symmetry activated:", self.symActicated)


    def checkModel(self, model):
        """
        [DEBUG FUNCTION]
        Check out if the given model satisfies basic property s.t. transitions
        follow a valid scheme, the id are correct, ...

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        delta = int(model.evaluate(self.delta).as_long())
        assert(delta == (self.BOUND - self.K - 1))

        previous = None
        for i in range(len(self.faultyPath)):
            v = int(model.evaluate(self.faultyPath[i]).as_long())
            if i > 0:
                lv = int(model.evaluate(self.lastlyActiveFaultyPath[i-1]).as_long())
            id = int(model.evaluate(self.idTransitionFaultyPath[i]).as_long())
            nop = model.evaluate(self.nopFaultyPath[i])
            assert(id == 0 or self.transitionList[v][2] == id)

            assert(nop or v != 0)
            if previous != None:
                assert(nop or self.transitionList[previous][1] == self.transitionList[v][0])
                print(lv, previous)
                assert(lv == previous)

            if not nop:
                previous = v

        previous = None
        for i in range(len(self.normalPath)):
            v = int(model.evaluate(self.normalPath[i]).as_long())
            if i > 0:
                lv = int(model.evaluate(self.lastlyActiveNormalPath[i-1]).as_long())
            id = int(model.evaluate(self.idTransitionNormalPath[i]).as_long())
            nop = model.evaluate(self.nopNormalPath[i])
            assert(id == 0 or self.transitionList[v][2] == id)

            assert(nop or v != 0)
            if previous != None:
                assert(nop or self.transitionList[previous][1] == self.transitionList[v][0])
                assert(lv == previous)

            if not nop:
                previous = v


    def printModel(self, model):
        """
        Print the model. That means information about the z3 variables and a output formal
        that can be considered for the checker.

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        print("[K DIAG CEGAR] cptFaultOccursByThePast: ")
        self.printOneIntArray(model, self.cptFaultOccursByThePast)

        print("[K DIAG CEGAR] Delta:")
        delta = int(model.evaluate(self.delta).as_long())
        print(delta, "=", self.BOUND, "-", self.K, "-", 1)

        super().printModel(model)


    def run(self):
        """
        Run the main program.
        """
        cpt = 1
        while cpt < (self.BOUND):
            cpt += 1
            self.incBound()

        self.s.add(self.cptFaultOccursByThePast[-1] - 1 > self.K)

        res = self.s.check()
        if res == sat:
            m = self.s.model()
            self.checkModel(m)
            self.printModel(m)
            return
        else:
            print("The problem is UNSAT")
