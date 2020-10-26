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
    limitFaulty = 0
    limitNoObser = 0
    observableId = []
    nextTransition = []
    possibleInitialTransition = []
    idxAssum = 0

    # z3 variables.
    faultyPath = [ Int("fp_1") ]
    normalPath = [ Int("np_1") ]
    idTransitionFaultyPath = [ Int("idt_fp_1") ]
    idTransitionNormalPath = [ Int("idt_np_1") ]
    nopFaultyPath = [ Bool("nop_fp_1") ]
    nopNormalPath = [ Bool("nop_np_1") ]
    faultOccursByThePast = [ Bool("faultOccurs_1") ]
    bound = Int("bound")
    k = Int("k")
    delta = Int("delta")


    def __init__(self, nameFile):
        """
        Constructor.

        :param nameFile: where is stored the automaton
        :type nameFile: str
        """
        # parse the file and store the automaton
        p = Parser()
        self.initState, self.transitionList = p.parse(nameFile)
        self.transitionList.sort(key=lambda t: t[2])

        self.nextTransition = [[] for i in range(len(self.transitionList))]
        for i in range(len(self.transitionList)):
            # fix the limit and store the id of the observable transitions.
            if self.transitionList[i][2] == 0:
                self.limitFaulty = i + 1
            elif self.transitionList[i][2] == 1:
                self.limitNoObser = i + 1
            else:
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

        # constraint on the first transition.
        self.s.add(Or([self.faultyPath[0] == v for v in self.possibleInitialTransition]))
        self.s.add(Or([self.normalPath[0] == v for v in self.possibleInitialTransition]))
        self.s.add(self.nopFaultyPath[0] == False)
        self.s.add(self.nopNormalPath[0] == False)
        self.s.add(self.delta == self.bound - self.k - 1)
        self.s.add(self.faultOccursByThePast[0] == (self.faultyPath[0] < self.limitFaulty))
        self.s.add(Implies(self.delta <= 0, self.faultOccursByThePast[0]))
        self.s.add(self.bound >= 0)
        self.s.add(self.k >= 0)

        self.addConstraintOnIdTransition(0)


    def addConstraintOnIdTransition(self, pos):
        """
        Add the constraint that fix the id of the transition pos in both
        idTransitionFaultyPath and idTransitionNormalPath.

        :param pos: the position of the operation we consider.
        :type pos: int
        """
        # two paths have to agree on the observables.
        # first we collect the id:
        self.s.add(Implies(self.faultyPath[pos] < self.limitNoObser, self.idTransitionFaultyPath[pos] == 0))
        self.s.add(Implies(self.normalPath[pos] < self.limitNoObser, self.idTransitionNormalPath[pos] == 0))

        for j in range(self.limitNoObser, len(self.transitionList)):
            self.s.add(Implies(self.faultyPath[pos] == j, self.idTransitionFaultyPath[pos] == self.transitionList[j][2]))
            self.s.add(Implies(self.normalPath[pos] == j, self.idTransitionNormalPath[pos] == self.transitionList[j][2]))

        # second we have an identical id
        self.s.add(self.idTransitionFaultyPath[pos] == self.idTransitionNormalPath[pos])


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

        # verify that transitions are correct.
        for j in range(len(self.transitionList)):
            if self.transitionList[j][2] >= 2:
                self.s.add(Implies(self.faultyPath[idx-1] == j, Or([self.faultyPath[idx] == n for n in self.nextTransition[j]])))
                self.s.add(Implies(self.normalPath[idx-1] == j, Or([self.normalPath[idx] == n for n in self.nextTransition[j]])))
            else:
                # we can always repeat no observable transition to simulate NOP.
                self.s.add(Implies(self.faultyPath[idx-1] == j, Or(self.faultyPath[idx] == j, Or([self.faultyPath[idx] == n for n in self.nextTransition[j]]))))
                self.s.add(Implies(self.normalPath[idx-1] == j, Or(self.normalPath[idx] == j, Or([self.normalPath[idx] == n for n in self.nextTransition[j]]))))

        # no fault in the normal path.
        self.s.add(self.normalPath[idx] >= self.limitFaulty)

        # we add the constraints that specify the id of the transition
        self.s.add(Implies(self.faultyPath[idx] < self.limitNoObser, self.idTransitionFaultyPath[idx] == 0))
        self.s.add(Implies(self.normalPath[idx] < self.limitNoObser, self.idTransitionNormalPath[idx] == 0))

        for j in range(self.limitNoObser, len(self.transitionList)):
            self.s.add(Implies(self.faultyPath[idx] == j, self.idTransitionFaultyPath[idx] == self.transitionList[j][2]))
            self.s.add(Implies(self.normalPath[idx] == j, self.idTransitionNormalPath[idx] == self.transitionList[j][2]))

        # we ensure that the id of the transition are the same for the normal and faulty paths (agree on the observable).
        self.s.add(self.idTransitionFaultyPath[idx] == self.idTransitionNormalPath[idx])

        # specify if the transition is a nop
        self.s.add(self.nopFaultyPath[idx] == (And(self.faultyPath[idx] < self.limitNoObser, self.faultyPath[idx-1] == self.faultyPath[idx])))
        self.s.add(self.nopNormalPath[idx] == (And(self.normalPath[idx] < self.limitNoObser, self.normalPath[idx-1] == self.normalPath[idx])))

        # we want to progress
        self.s.add(Or(Not(self.nopFaultyPath[idx]), Not(self.nopNormalPath[idx])))

        # breaking symmetries in the nop schema
        self.s.add(Implies(self.nopFaultyPath[idx-1], Or(self.nopFaultyPath[idx], self.idTransitionFaultyPath[idx] != 0)))
        self.s.add(Implies(self.nopNormalPath[idx-1], Or(self.nopNormalPath[idx], self.idTransitionNormalPath[idx] != 0)))

        # the dynamic of the fault list of variables
        self.s.add(Or(self.faultOccursByThePast[idx-1], self.faultyPath[idx] < self.limitFaulty) == self.faultOccursByThePast[idx])

        # # we have a fault soon enough.
        self.s.add(Implies(self.delta <= idx, self.faultOccursByThePast[idx]))



    def printAutomatonInfo(self):
        """
        Print information about the given automaton
        """
        print("Information ...")
        print("automata:")
        for i in range(len(self.transitionList)):
            print(i, ":", self.transitionList[i])

        print("next transition:")
        for i in range(len(self.nextTransition)):
            print(i, ':', self.nextTransition[i])

        print("possible init transition: ", self.possibleInitialTransition)
        print("limitFaulty:", self.limitFaulty)
        print("limitNoObser:", self.limitNoObser)


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
        assert(delta == (bound - k))

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


    def run(self):
        """
        Run the main program.
        """
        for i in range(4):
            self.incBound()

        # assumption:
        self.idxAssum += 1
        assumB = Bool("b" + str(self.idxAssum))
        self.s.add(Implies(assumB, self.bound == len(self.faultyPath)))
        assumK = Bool("k" + str(self.idxAssum))
        self.s.add(Implies(assumK, self.k == 1))
        self.printZ3Constraints()

        res = self.s.check(assumB, assumK)
        if res == sat:
            m = self.s.model()
            # self.checkModel(m)

            print("Delta:")
            delta = int(m.evaluate(self.delta).as_long())
            bound = int(m.evaluate(self.bound).as_long())
            k = int(m.evaluate(self.k).as_long())
            print(delta, "=", bound, "-", k, "-", 1)
            print()

            # print the paths
            print("Faulty path:")
            for i in range(len(self.faultyPath)):
                v = int(m.evaluate(self.faultyPath[i]).as_long())
                id = int(m.evaluate(self.idTransitionFaultyPath[i]).as_long())
                nop = m.evaluate(self.nopFaultyPath[i])
                inFault = m.evaluate(self.faultOccursByThePast[i])
                print(self.transitionList[v],id,nop,inFault)
            print()

            print("Normal path:")
            for i in range(len(self.normalPath)):
                v = int(m.evaluate(self.normalPath[i]).as_long())
                id = int(m.evaluate(self.idTransitionNormalPath[i]).as_long())
                nop = m.evaluate(self.nopNormalPath[i])
                print(self.transitionList[v],id,nop)
            print()
        else:
            print("it is unsat")

# the solver instance.

# the automata.
assert(len(sys.argv) == 2)
z3Model = Z3Model(sys.argv[1])
z3Model.printAutomatonInfo()
z3Model.run()
