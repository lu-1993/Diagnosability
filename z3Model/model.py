#!/usr/bin/python3
# -*- coding: utf-8 -*-

from z3 import *
from parser import Parser

# Here are some suppositions:
# The NOP operation is represented by the ID 0
# The faulty transition is labelled with 1
# A non observable transition is labelled with 2

class Z3Model:
    # z3 solver.
    s = Solver()

    # automaton description.
    initState = 0
    transitionList = []
    nextTransition = []
    idxAssum = 0
    maxLabelTransition = 0
    maxLabelState = 0

    # z3 variables.
    labelTransition = []
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
    cptFaultOccursByThePast = [ Int("cptFaultOccurs_1") ]
    bound = Int("bound")
    k = Int("k")
    delta = Int("delta")

    # parameter
    BOUND = 0
    K = 0

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
        # parse the file and store the automaton
        p = Parser()
        self.initState, self.transitionList, self.BOUND, self.K = p.parse(nameFile)

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

        # we assign a status for each transition.
        self.labelTransition = [ Int("statusTransition_" + str(i+1)) for i in range(len(self.transitionList))]

        # the first transition is labelled with 0: it is the NOP transition
        self.s.add(self.labelTransition[0] == 0)

        # The status for a transition can be 0 for a NOP, 1 for fault, 2 for an non observable and at least 3 for an observable event.
        self.s.add(And([And(x >= 0, x <= self.maxLabelTransition) for x in self.labelTransition]))

        # constraint on the first transition: cannot be nop by construction of possibleInitialTransition.
        self.s.add(self.faultyPath[0] == len(self.transitionList) - 1)
        self.s.add(self.normalPath[0] == len(self.transitionList) - 1)
        self.s.add(self.faultyPath[0] == self.lastlyActiveFaultyPath[0])
        self.s.add(self.normalPath[0] == self.lastlyActiveNormalPath[0])

        self.s.add(self.idTransitionNormalPath[0] != self.FAULT)
        self.s.add(self.nopFaultyPath[0] == False)
        self.s.add(self.nopNormalPath[0] == False)
        self.s.add(self.delta == self.bound - self.k - 1)
        self.s.add(self.faultOccursByThePast[0] == (self.idTransitionFaultyPath[0] == self.FAULT))
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
        # collect the label for the transition
        for j in range(len(self.transitionList)):
            self.s.add(Implies(self.faultyPath[pos] == j, self.idTransitionFaultyPath[pos] == self.labelTransition[j]))
            self.s.add(Implies(self.normalPath[pos] == j, self.idTransitionNormalPath[pos] == self.labelTransition[j]))

        # it is useless to go more than k after the first occurrence of the fault (=> we do not care if the critical pair is divergente).
        # two paths have to agree on the observables.
        self.s.add(Or(self.idTransitionFaultyPath[pos] > self.NO_OBS, self.idTransitionNormalPath[pos] > self.NO_OBS) == self.checkSynchro[pos])

        # count since when the first fault occurs
        self.s.add(Or(self.cptFaultOccursByThePast[pos] - 1 > self.k, Not(self.checkSynchro[pos]), self.idTransitionFaultyPath[pos] == self.idTransitionNormalPath[pos]))


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
        self.faultOccursByThePast.append(Bool("faultOccurs_" + str(idx)))
        self.nopNormalPath.append(Bool("nop_np_" + str(idx)))
        self.cptFaultOccursByThePast.append(Int("cptFaultOccurs_" + str(idx)))
        self.checkSynchro.append(Bool("checkSynchro_" + str(idx)))


    def incBound(self):
        """
        Extend the bound allowing a new transition.
        """
        idx = len(self.faultyPath)
        assert(idx > 0)

        self.incVariableList()

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

        # verify that transitions are correct regarding the label.
        for j in range(len(self.transitionList)):
            self.s.add(Implies(self.lastlyActiveFaultyPath[idx-1] == j, Or([self.faultyPath[idx] == n for n in self.nextTransition[j]])))
            self.s.add(Implies(self.lastlyActiveNormalPath[idx-1] == j, Or([self.normalPath[idx] == n for n in self.nextTransition[j]])))

        # no fault in the normal path.
        self.s.add(self.idTransitionNormalPath[idx] != self.FAULT)

        # we add the constraints that specify the id of the transition
        self.addConstraintOnIdTransition(idx)

        # specify if the transition is a nop
        self.s.add(self.nopFaultyPath[idx] == (self.faultyPath[idx] == self.NOP_TRANSITION))
        self.s.add(self.nopNormalPath[idx] == (self.normalPath[idx] == self.NOP_TRANSITION))

        # we want to progress
        self.s.add(Or(Not(self.nopFaultyPath[idx]), Not(self.nopNormalPath[idx])))

        # breaking symmetries in the nop schema
        self.s.add(Implies(self.nopFaultyPath[idx-1], Or(self.nopFaultyPath[idx], self.idTransitionFaultyPath[idx] > self.NO_OBS)))
        self.s.add(Implies(self.nopNormalPath[idx-1], Or(self.nopNormalPath[idx], self.idTransitionNormalPath[idx] > self.NO_OBS)))

        # the dynamic of the fault list of variables
        self.s.add(Or(self.faultOccursByThePast[idx-1], self.idTransitionFaultyPath[idx] == self.FAULT) == self.faultOccursByThePast[idx])

        # we have a fault soon enough.
        self.s.add(Implies(self.delta <= idx, self.faultOccursByThePast[idx]))

        # set the counter since when the fault occurs.
        self.s.add(self.cptFaultOccursByThePast[idx] == self.cptFaultOccursByThePast[idx-1] + (And(self.faultyPath[idx] != self.NOP_TRANSITION, self.faultOccursByThePast[idx])))


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
        print("lastlyActiveFaultyPath")
        self.printOneIntArray(model, self.lastlyActiveFaultyPath)
        print("lastlyActiveNormalPath")
        self.printOneIntArray(model, self.lastlyActiveNormalPath)
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
        print("checkSynchro")
        self.printOneBoolArray(model, self.checkSynchro)
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
        while cpt < (2 * self.BOUND):
            cpt += 1
            self.incBound()

            # assumption:
            self.idxAssum += 1
            assumB = Bool("b" + str(self.idxAssum))    # fix the bound
            assumF = Bool("f" + str(self.idxAssum))    # ensure that we have enough real transition at the end

            self.s.add(Implies(assumB, self.bound == len(self.faultyPath)))
            self.s.add(Implies(assumF, self.cptFaultOccursByThePast[-1] - 1 > self.k))

            res = self.s.check(assumB, assumK, assumF)
            if res == sat:
                m = self.s.model()
                self.checkModel(m)
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
