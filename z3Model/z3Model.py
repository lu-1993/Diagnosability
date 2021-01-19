#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from z3 import *
from model import Model

class Z3Model (Model):
    # z3 solver.
    s = Solver()

    faultyPath = [ Int("fp_1") ]
    normalPath = [ Int("np_1") ]

    lastlyActiveFaultyPath = [ Int("lfp_1") ]
    lastlyActiveNormalPath = [ Int("lnp_1") ]
    idTransitionFaultyPath = [ Int("idt_fp_1") ]
    idTransitionNormalPath = [ Int("idt_np_1") ]
    nopFaultyPath = [ Bool("nop_fp_1") ]
    nopNormalPath = [ Bool("nop_np_1") ]
    faultOccursByThePast = [ Bool("faultOccurs_1") ]
    checkSynchro = [ Bool("check_synchro_1") ]

    # classic variable.
    symActicated = False

    def incVariableList(self):
        """
        Increment all the list with one new z3 variable.
        """
        idx = len(self.faultyPath) + 1
        self.faultyPath.append(Int("fp_" + str(idx)))
        self.normalPath.append(Int("np_" + str(idx)))
        self.lastlyActiveFaultyPath.append(Int("lfp_" + str(idx)))
        self.lastlyActiveNormalPath.append(Int("lnp_" + str(idx)))
        self.idTransitionFaultyPath.append(Int("idt_fp_" + str(idx)))
        self.idTransitionNormalPath.append(Int("idt_np_" + str(idx)))
        self.nopFaultyPath.append(Bool("nop_fp_" + str(idx)))
        self.nopNormalPath.append(Bool("nop_np_" + str(idx)))
        self.faultOccursByThePast.append(Bool("faultOccurs_" + str(idx)))


    def incBound(self):
        """
        Extend the bound allowing a new transition.
        """
        idx = len(self.faultyPath) - 1

        # we reduce the domain to what it is necessary
        self.s.add(self.faultyPath[idx] <= len(self.transitionList))
        self.s.add(self.normalPath[idx] <= len(self.transitionList))

        self.s.add(self.idTransitionFaultyPath[idx] <= self.maxLabelTransition)
        self.s.add(self.idTransitionNormalPath[idx] <= self.maxLabelTransition)

        # set the lastly active transition.
        self.s.add(Implies(self.faultyPath[idx] == self.NOP_TRANSITION, self.lastlyActiveFaultyPath[idx] == self.lastlyActiveFaultyPath[idx-1]))
        self.s.add(Implies(self.faultyPath[idx] != self.NOP_TRANSITION, self.lastlyActiveFaultyPath[idx] == self.faultyPath[idx]))
        self.s.add(Implies(self.normalPath[idx] == self.NOP_TRANSITION, self.lastlyActiveNormalPath[idx] == self.lastlyActiveNormalPath[idx-1]))
        self.s.add(Implies(self.normalPath[idx] != self.NOP_TRANSITION, self.lastlyActiveNormalPath[idx] == self.normalPath[idx]))

        # verifying that transitions are correct regarding the label.
        for j in range(len(self.transitionList)):
            self.s.add(Implies(self.lastlyActiveFaultyPath[idx-1] == j, Or([self.faultyPath[idx] == n for n in self.nextTransition[j]])))
            self.s.add(Implies(self.lastlyActiveNormalPath[idx-1] == j, Or([self.normalPath[idx] == n for n in self.nextTransition[j]])))

        # no fault in the normal path.
        self.s.add(self.idTransitionNormalPath[idx] != self.FAULT)

        # we want to progress
        self.s.add(Or(Not(self.nopFaultyPath[idx]), Not(self.nopNormalPath[idx])))

        # specify if the transition is a nop
        self.s.add(self.nopFaultyPath[idx] == (self.faultyPath[idx] == self.NOP_TRANSITION))
        self.s.add(self.nopNormalPath[idx] == (self.normalPath[idx] == self.NOP_TRANSITION))

        # the dynamic of the fault list of variables
        self.s.add(Or(self.faultOccursByThePast[idx-1], self.idTransitionFaultyPath[idx] == self.FAULT) == self.faultOccursByThePast[idx])

        # breaking symmetries in the nop schema
        if self.symActicated:
            self.s.add(Implies(self.nopFaultyPath[idx-1], Or(self.nopFaultyPath[idx], self.idTransitionFaultyPath[idx] > self.NO_OBS)))
            self.s.add(Implies(self.nopNormalPath[idx-1], Or(self.nopNormalPath[idx], self.idTransitionNormalPath[idx] > self.NO_OBS)))



    def printOneIntArray(self, model, array):
        """
        Print a list of z3 variables.

        :param model: the model we want to check.
        :type model: a z3 model.
        :param array: the list of z3 variables we want to print out.
        :type model: list of integer z3 variables.
        """
        for x in array:
            print('{:-6}'.format(int(model.evaluate(x).as_long())),end=" ")
        print()

    def printOneBoolArray(self, model, array):
        """
        Print a list of z3 variables.

        :param model: the model we want to check.
        :type model: a z3 model.
        :param array: the list of z3 variables we want to print out.
        :type model: list of boolean z3 variables.
        """
        for x in array:
            r = model.evaluate(x)
            id = 0
            if r:
                id = 1
            print('{:-6}'.format(id),end=" ")
        print()


    def printModel(self, model):
        """
        Print out the status of the different variables regarding a given model.

        :param model: the model we want to print.
        :type model: a z3 model.
        """
        print("[Z3 model] faultyPath: ")
        self.printOneIntArray(model, self.faultyPath)
        print("[Z3 model] normalPath: ")
        self.printOneIntArray(model, self.normalPath)
        print("[Z3 model] lastlyActiveFaultyPath")
        self.printOneIntArray(model, self.lastlyActiveFaultyPath)
        print("[Z3 model] lastlyActiveNormalPath")
        self.printOneIntArray(model, self.lastlyActiveNormalPath)
        print("[Z3 model] idTransitionFaultyPath: ")
        self.printOneIntArray(model, self.idTransitionFaultyPath)
        print("[Z3 model] idTransitionNormalPath: ")
        self.printOneIntArray(model, self.idTransitionNormalPath)
        print("[Z3 model] nopFaultyPath:")
        self.printOneBoolArray(model, self.nopFaultyPath)
        print("[Z3 model] nopNormalPath: ")
        self.printOneBoolArray(model, self.nopNormalPath)
        print("[Z3 model] faultOccursByThePast: ")
        self.printOneBoolArray(model, self.faultOccursByThePast)
        print("[Z3 model] checkSynchro")
        self.printOneBoolArray(model, self.checkSynchro)

        # print the paths
        print("[Z3 model] Faulty path:")
        for i in range(len(self.faultyPath)):
            v = int(model.evaluate(self.faultyPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionFaultyPath[i]).as_long())
            nop = model.evaluate(self.nopFaultyPath[i])
            inFault = model.evaluate(self.faultOccursByThePast[i])
            print(self.transitionList[v], id, nop, inFault)
        print()

        print("[Z3 model] Normal path:")
        for i in range(len(self.normalPath)):
            v = int(model.evaluate(self.normalPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionNormalPath[i]).as_long())
            nop = model.evaluate(self.nopNormalPath[i])
            print(self.transitionList[v], id, nop)
        print()

    def printZ3Constraints(self):
        """
        Print the constraint store in the solver following the z3 format.
        """
        print(self.s)
