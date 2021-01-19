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
