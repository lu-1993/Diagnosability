#!/usr/bin/python3
# -*- coding: utf-8 -*-

from z3 import *
from parser import Parser

# Here are some suppositions:
# The NOP operation is represented by no observable that repeat.

class Z3Model:
    # z3 solver.
    s = Solver()

    # automaton description.
    initState = 0
    transitionList = []
    observableId = []
    nextTransition = []
    possibleInitialTransition = []
    idxAssum = 0

    # z3 variables.
    labelTransition = []
    faultyPath = [ Int("fp_1") ]
    normalPath = [ Int("np_1") ]
    idTransitionFaultyPath = [ Int("idt_fp_1") ]
    idTransitionNormalPath = [ Int("idt_np_1") ]
    nopFaultyPath = [ Bool("nop_fp_1") ]
    nopNormalPath = [ Bool("nop_np_1") ]
    faultOccursByThePast = [ Bool("faultOccurs_1") ]
    cptFaultOccursByThePast = [ Int("cptFaultOccurs_1") ]
    bound = Int("bound")
    k = Int("k")
    delta = Int("delta")

    # parameter
    BOUND = 0
    K = 0

    def __init__(self, nameFile):
        """
        Constructor.

        :param nameFile: where is stored the automaton
        :type nameFile: str
        """
        # parse the file and store the automaton
        p = Parser()
        self.initState, self.transitionList, self.BOUND, self.K = p.parse(nameFile)
        # self.transitionList.sort(key=lambda t: t[2])

        self.nextTransition = [[] for i in range(len(self.transitionList))]
        for i in range(len(self.transitionList)):
            # fix the limit and store the id of the observable transitions.
            if self.transitionList[i][2] > 1:
                if self.transitionList[i][2] not in self.observableId:
                    self.observableId.append(self.transitionList[i][2])

            # for a transition t, collect the list of possible next transition that can be executed after t.
            for j in range(len(self.transitionList)):
                if (self.transitionList[i][1] == self.transitionList[j][0]):
                    self.nextTransition[i].append(j)

        # get the transition that are valid with the initial init state.
        for i in range(len(self.transitionList)):
            if self.transitionList[i][0] == self.initState:
                self.possibleInitialTransition.append(i)

        # we assign a status for each transition.
        self.labelTransition = [ Int("statusTransition_" + str(i+1)) for i in range(len(self.transitionList))]

        # The status for a transition can be 0 for a fault, 1 for an non observable and 2 for an observable event.
        for x in self.labelTransition:
            self.s.add(And(x >= 0, x <= len(self.observableId) + 2))

        # constraint on the first transition.
        self.s.add(Or([self.faultyPath[0] == v for v in self.possibleInitialTransition]))
        self.s.add(Or([self.normalPath[0] == v for v in self.possibleInitialTransition]))
        self.s.add(self.idTransitionNormalPath[0] != 0)
        self.s.add(self.nopFaultyPath[0] == False)
        self.s.add(self.nopNormalPath[0] == False)
        self.s.add(self.delta == self.bound - self.k - 1)
        self.s.add(self.faultOccursByThePast[0] == (self.idTransitionFaultyPath[0] == 0))
        self.s.add(Implies(self.delta <= 0, self.faultOccursByThePast[0]))
        self.s.add(self.bound >= 0)
        self.s.add(self.k >= 0)
        self.s.add(self.cptFaultOccursByThePast[0] == self.faultOccursByThePast[0])

        self.addConstraintOnIdTransition(0)


    def addConstraintOnIdTransition(self, pos):
        """
        Add the constraint that fix the id of the transition pos in both
        idTransitionFaultyPath and idTransitionNormalPath.

        :param pos: the position of the operation we consider.
        :type pos: int
        """
        # two paths have to agree on the observables.
        for j in range(len(self.transitionList)):
            self.s.add(Implies(self.faultyPath[pos] == j, self.idTransitionFaultyPath[pos] == self.labelTransition[j]))
            self.s.add(Implies(self.normalPath[pos] == j, self.idTransitionNormalPath[pos] == self.labelTransition[j]))

        # it is useless to go more than k after the first occurrence of the fault (=> we do not care if the critical pair is divergente).
        self.s.add(Or(self.cptFaultOccursByThePast[pos] - 1 > self.k, self.idTransitionFaultyPath[pos] == self.idTransitionNormalPath[pos]))


    def incVariableList(self):
        """
        Increment all the list with one new z3 variable.
        """
        idx = len(self.faultyPath) + 1
        self.faultyPath.append(Int("fp_" + str(idx)))
        self.normalPath.append(Int("np_" + str(idx)))
        self.idTransitionFaultyPath.append(Int("idt_fp_" + str(idx)))
        self.idTransitionNormalPath.append(Int("idt_np_" + str(idx)))
        self.nopFaultyPath.append(Bool("nop_fp_" + str(idx)))
        self.faultOccursByThePast.append(Bool("faultOccurs_" + str(idx)))
        self.nopNormalPath.append(Bool("nop_np_" + str(idx)))
        self.cptFaultOccursByThePast.append(Int("cptFaultOccurs_" + str(idx)))


    def incBound(self):
        """
        Extend the bound allowing a new transition.
        """
        idx = len(self.faultyPath)
        assert(idx > 0)

        self.incVariableList()

        # we reduce the domain to what it is necessary
        self.s.add(self.faultyPath[idx] < len(self.transitionList))
        self.s.add(self.normalPath[idx] < len(self.transitionList))

        self.s.add(self.idTransitionFaultyPath[idx] < len(self.observableId) + 2)
        self.s.add(self.idTransitionNormalPath[idx] < len(self.observableId) + 2)

        # verify that transitions are correct regarding the label.
        for j in range(len(self.transitionList)):
            self.s.add(Implies(And(self.faultyPath[idx-1] == j, self.labelTransition[idx-1] >= 0), Or([self.faultyPath[idx] == n for n in self.nextTransition[j]])))
            self.s.add(Implies(And(self.normalPath[idx-1] == j, self.labelTransition[idx-1] >= 0), Or([self.normalPath[idx] == n for n in self.nextTransition[j]])))
            self.s.add(Implies(And(self.faultyPath[idx-1] == j, self.labelTransition[idx-1] >= 0), Or(self.faultyPath[idx] == j, Or([self.faultyPath[idx] == n for n in self.nextTransition[j]]))))
            self.s.add(Implies(And(self.normalPath[idx-1] == j, self.labelTransition[idx-1] >= 0), Or(self.normalPath[idx] == j, Or([self.normalPath[idx] == n for n in self.nextTransition[j]]))))


        # no fault in the normal path.
        self.s.add(self.idTransitionNormalPath[idx] != 0)

        # we add the constraints that specify the id of the transition
        self.addConstraintOnIdTransition(idx)

        # specify if the transition is a nop
        self.s.add(self.nopFaultyPath[idx] == (And(self.idTransitionFaultyPath[idx] < 2, self.faultyPath[idx-1] == self.faultyPath[idx])))
        self.s.add(self.nopNormalPath[idx] == (And(self.idTransitionNormalPath[idx] < 2, self.normalPath[idx-1] == self.normalPath[idx])))

        # we want to progress
        self.s.add(Or(Not(self.nopFaultyPath[idx]), Not(self.nopNormalPath[idx])))

        # breaking symmetries in the nop schema
        self.s.add(Implies(self.nopFaultyPath[idx-1], Or(self.nopFaultyPath[idx], self.idTransitionFaultyPath[idx] != 0)))
        self.s.add(Implies(self.nopNormalPath[idx-1], Or(self.nopNormalPath[idx], self.idTransitionNormalPath[idx] != 0)))

        # the dynamic of the fault list of variables
        self.s.add(Or(self.faultOccursByThePast[idx-1], self.idTransitionFaultyPath[idx] == 1) == self.faultOccursByThePast[idx])

        # we have a fault soon enough.
        self.s.add(Implies(self.delta <= idx, self.faultOccursByThePast[idx]))

        # set the counter since when the fault occurs.
        self.s.add(self.cptFaultOccursByThePast[idx] == self.cptFaultOccursByThePast[idx-1] + self.faultOccursByThePast[idx])


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

        print("possible init transition: ", self.possibleInitialTransition)
        print("BOUND:", self.BOUND)
        print("K:", self.K)



    def printZ3Constraints(self):
        """
        Print the constraint store in the solver following the z3 format.
        """
        print(self.s)


    def checkModel(self, model):
        """
        [DEBUG FUNCTION]
        Check out if the given model satisfies basic property s.t. transitions
        follow a valid scheme, the id are correct, ...

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        delta = int(model.evaluate(self.delta).as_long())
        bound = int(model.evaluate(self.bound).as_long())
        k = int(model.evaluate(self.k).as_long())
        assert(delta == (bound - k - 1))

        previous = None
        for i in range(len(self.faultyPath)):
            v = int(model.evaluate(self.faultyPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionFaultyPath[i]).as_long())
            nop = model.evaluate(self.nopFaultyPath[i])
            assert(id == 0 or self.transitionList[v][2] == id)

            if previous != None:
                assert(nop or self.transitionList[previous][1] != self.transitionList[v][0])
            previous = v

        previous = None
        for i in range(len(self.normalPath)):
            v = int(model.evaluate(self.normalPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionNormalPath[i]).as_long())
            nop = model.evaluate(self.nopNormalPath[i])
            assert(id == 0 or self.transitionList[v][2] == id)

            if previous != None:
                assert(nop or self.transitionList[previous][1] != self.transitionList[v][0])
            previous = v


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
        Print the model. That means information about the z3 variables and a output formal
        that can be considered for the checker.

        :param model: the model we want to check.
        :type model: a z3 model.
        """
        print("--------------------")
        print("z3 arrays (size = " + str(len(self.faultyPath)) + ")")
        print("--------------------")
        print("faultyPath: ")
        self.printOneIntArray(model, self.faultyPath)
        print("normalPath: ")
        self.printOneIntArray(model, self.normalPath)
        print("idTransitionFaultyPath: ")
        self.printOneIntArray(model, self.idTransitionFaultyPath)
        print("idTransitionNormalPath: ")
        self.printOneIntArray(model, self.idTransitionNormalPath)
        print("cptFaultOccursByThePast: ")
        self.printOneIntArray(model, self.cptFaultOccursByThePast)
        print("nopFaultyPath:")
        self.printOneBoolArray(model, self.nopFaultyPath)
        print("nopNormalPath: ")
        self.printOneBoolArray(model, self.nopNormalPath)
        print("faultOccursByThePast: ")
        self.printOneBoolArray(model, self.faultOccursByThePast)
        print("labelTransition")
        self.printOneIntArray(model, self.labelTransition)
        print()

        print("Delta:")
        delta = int(model.evaluate(self.delta).as_long())
        bound = int(model.evaluate(self.bound).as_long())
        k = int(model.evaluate(self.k).as_long())
        print(delta, "=", bound, "-", k, "-", 1)
        print()

        # print the paths
        print("Faulty path:")
        for i in range(len(self.faultyPath)):
            v = int(model.evaluate(self.faultyPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionFaultyPath[i]).as_long())
            nop = model.evaluate(self.nopFaultyPath[i])
            inFault = model.evaluate(self.faultOccursByThePast[i])
            print(self.transitionList[v],id,nop,inFault)
        print()

        print("Normal path:")
        for i in range(len(self.normalPath)):
            v = int(model.evaluate(self.normalPath[i]).as_long())
            id = int(model.evaluate(self.idTransitionNormalPath[i]).as_long())
            nop = model.evaluate(self.nopNormalPath[i])
            print(self.transitionList[v],id,nop)
        print()


    def run(self):
        """
        Run the main program.
        """
        assumK = Bool("k" + str(self.idxAssum))
        self.s.add(Implies(assumK, self.k == self.K))

        # run in normal mode
        for i in range(len(self.transitionList)):
            self.s.add(self.labelTransition[i] == self.transitionList[i][2])

        cpt = 1
        while cpt < self.BOUND:
            cpt += 1
            self.incBound()

            # assumption:
            self.idxAssum += 1
            assumB = Bool("b" + str(self.idxAssum))
            self.s.add(Implies(assumB, self.bound == len(self.faultyPath)))

            res = self.s.check(assumB, assumK)
            if res == sat:
                m = self.s.model()
                # self.checkModel(m)
                self.printModel(m)
                return
            else:
                print("Increase the bound:", len(self.faultyPath) + 1)

        print("The problem is UNSAT")

# the automata.
assert(len(sys.argv) == 2)
z3Model = Z3Model(sys.argv[1])
z3Model.printAutomatonInfo()
z3Model.run()
