#!/usr/bin/python3
# -*- coding: utf-8 -*-

from z3 import Solver, Int, Bool, Real, Implies, And, If, Or, Not, sat
from parsertT import Parser
from fractions import Fraction

from automaton import Automaton


import time
import sys

# Here are some suppositions:
# The NOP operation is represented by the ID 0
# The faulty transition is labelled with 1
# A non observable transition is labelled with 2


class Z3Model:
    """
    Class to represent the z3 model of time automaton
    """
    # 'constants'
    NOP = 0
    FAULT = 1
    NO_OBS = 2
    NOP_TRANSITION = 0

    def __init__(self):
        # z3 solver.
        self.s = Solver()

        # parse the file and store the automaton
        self.p = Parser()
        self.automaton, self.BOUND, self.DELTA = self.p.parse(
            sys.argv[1])

        # automaton description.
        self.initState = 0
        # transitionList = []
        self.nextTransition = []   # this list only store index of the transitions
        self.idxAssum = 0
        self.maxLabelTransition = 0
        self.maxLabelState = 0

        # z3 variables.
        self.labelTransition = []
        self.clockTransition = []

        self.faultyPath = [Int("fp_1")]
        self.normalPath = [Int("np_1")]
        self.lastlyActiveFaultyPath = [Int("lfp_1")]
        self.lastlyActiveNormalPath = [Int("lnp_1")]
        self.idTransitionFaultyPath = [Int("idt_fp_1")]
        self.idTransitionNormalPath = [Int("idt_np_1")]
        self.nopFaultyPath = [Bool("nop_fp_1")]
        self.nopNormalPath = [Bool("nop_np_1")]
        self.faultOccursByThePast = [Bool("faultOccurs_1")]
        self.checkSynchro = [Bool("check_synchro_1")]
        self.cptFaultOccursByThePast = [
            Real("cptFaultOccurs_1")]  # store delta
        self.cptFaultOccursByThePast.append(Real("cptFaultOccurs_2"))

        self.globalClockFaultyPath = [Real("g_fp_1")]
        self.globalClockNormalPath = [Real("g_np_1")]

        self.delayClockFaultyPath = [Real("delay_fp_1")]
        self.delayClockNormalPath = [Real("delay_np_1")]
        self.delayClockFaultyPath.append(Real("delay_fp_2"))
        self.delayClockNormalPath.append(Real("delay_np_2"))

        self.clockConstraintFaultyPath = [Bool("constraint_fp_1")]
        self.clockConstraintNormalPath = [Bool("constraint_np_1")]

        # clockConstraint[clock_number][transition_number]
        self.clockValueFaultyPath = [
            [Real("clock"+str(i+1)+"_fp_1"), Real("clock"+str(i+1)+"_fp_2")] for i in range(self.automaton.clockNum)]

        self.clockValueNormalPath = [
            [Real("clock"+str(i+1)+"_np_1"), Real("clock"+str(i+1)+"_np_2")] for i in range(self.automaton.clockNum)]

        self.sourceInvFaultyPath = [
            [Bool("sourceInv"+str(i+1)+'_fp_1')] for i in range(self.automaton.clockNum)]
        self.sourceInvNormalPath = [
            [Bool("sourceInv"+str(i+1)+'_np_1')] for i in range(self.automaton.clockNum)]
        self.finalInvFaultyPath = [
            [Bool("finalInv"+str(i+1)+'_fp_1')] for i in range(self.automaton.clockNum)]
        self.finalInvNormalPath = [
            [Bool("finalInv"+str(i+1)+'_np_1')] for i in range(self.automaton.clockNum)]

        self.lengthFaultyPath = [Int("length_fp_1")]
        self.lengthNormalPath = [Int("normal_np_1")]

        self.resetConstraintFaultyPath = [
            [Bool("reset" + str(i + 1) + "_fp_1")] for i in range(self.automaton.clockNum)]
        self.resetConstraintNormalPath = [
            [Bool("reset" + str(i + 1) + "_np_1")] for i in range(self.automaton.clockNum)]

        self.bound = Int("bound")
        self.delta = Int("delta")

        # we add a transition, that is the nop transition, in position 0 in the transitionList
        self.nextTransition = [[self.NOP_TRANSITION] for i in range(
            self.automaton.getNbTransition())]  # they can all do nop

        self.maxLabelState = self.automaton.getMaxStateLabel()

        transitionList = self.automaton.getTransitionList()
        for i in range(self.automaton.getNbTransition()):
            # for a transition t, collect the list of possible next transition that can be executed after t.
            for j in range(self.automaton.getNbTransition()):
                if (transitionList[i].getFinalState() == transitionList[j].getSourceState()):
                    self.nextTransition[i].append(j)

        # we add a transition to start the two path identically.
        self.maxLabelState += 1

        ####################################
        self.automaton.addState(self.maxLabelState, 1)
        self.automaton.appendTransition(self.maxLabelState, self.initState, 2, [
                                        'c' + str(i+1) + "=0" for i in range(self.automaton.clockNum)], list(range(self.automaton.clockNum)))

        # we add the transition is the last one in the transitionList , so the last one nextTransition is idx: idx is transition which begin with initState.
        self.nextTransition.append([self.NOP_TRANSITION])
        self.nextTransition[-1] += [idx for idx in range(
            self.automaton.getNbTransition()) if transitionList[idx].getSourceState() == self.automaton.getInitialState()]

        # we assign a status for each transition.
        self.labelTransition = [Int("statusTransition_" + str(i+1))
                                for i in range(self.automaton.getNbTransition())]

        # we assign reset constraint for each transtion
        self.resetTransition = [
            [False for j in range(self.automaton.getNbTransition())] for i in range(self.automaton.clockNum)]
        for i in range(self.automaton.getNbTransition()):
            for c in self.automaton.getTransitionAt(i).getResetList():
                self.resetTransition[c][i] = True

        # we assign a clock constraints in clockTransition list in order.
        for i in range(self.automaton.getNbTransition()):
            self.clockTransition.append(
                self.automaton.getTransitionAt(i).getGuard())

        for t in self.automaton.getTransitionList():  # max label of transitions
            if t.getEventId() > self.maxLabelTransition:
                self.maxLabelTransition = t.getEventId()

        # the first transition is labelled with 0: it is the NOP transition NOP: event = 0
        # event = 0
        self.s.add(self.labelTransition[0] == 0)

        # The status for a transition can be 0 for a NOP, 1 for fault, 2 for an non observable and at least 3 for an observable event.
        self.s.add(And([And(x >= 0, x <= self.maxLabelTransition)
                   for x in self.labelTransition]))

        # constraint on the first transition: cannot be nop by construction of possibleInitialTransition.
        # the last one in transitionList, which we add.
        self.s.add(self.faultyPath[0] == self.automaton.getNbTransition() - 1)
        self.s.add(self.normalPath[0] == self.automaton.getNbTransition() - 1)
        self.s.add(self.faultyPath[0] == self.lastlyActiveFaultyPath[0])
        self.s.add(self.normalPath[0] == self.lastlyActiveNormalPath[0])

        # all clocks are initialized to 0 in the first transition
        for i in range(self.automaton.clockNum):
            self.s.add(self.clockValueFaultyPath[i][0] == 0)
            self.s.add(self.clockValueNormalPath[i][0] == 0)

        # global clock is initialized to 0 in the first transition
        self.s.add(self.globalClockFaultyPath[0] == 0)
        self.s.add(self.globalClockNormalPath[0] == 0)

        self.s.add(self.idTransitionNormalPath[0] != self.FAULT)
        self.s.add(self.nopFaultyPath[0] == False)
        self.s.add(self.nopNormalPath[0] == False)

        self.s.add(self.faultOccursByThePast[0] == (
            self.idTransitionFaultyPath[0] == self.FAULT))
        self.s.add(self.cptFaultOccursByThePast[0] == 0)
        self.s.add(self.bound >= 0)
        self.s.add(self.delta >= 0)

        # delay of first faulty and normal path are initialized to 0.
        self.s.add(self.delayClockFaultyPath[0] == 0)
        self.s.add(self.delayClockNormalPath[0] == 0)

        # the first transition is we added, so we do not count it.
        self.s.add(self.lengthNormalPath[0] == 0)
        self.s.add(self.lengthFaultyPath[0] == 0)

        self.isObservableTransition = [Bool(
            "isObservable_" + str(i + 1)) for i in range(self.automaton.getNbTransition())]
        self.addConstraintOnIdTransition(0)

    def addConstraintOnIdTransition(self, pos):
        """
        Add the constraint that fix the id of the transition pos in both
        idTransitionFaultyPath and idTransitionNormalPath.

        :param pos: the position of the operation we consider.
        :type pos: int
        """
        # collect the label for the transition

        for j in range(self.automaton.getNbTransition()):

            # assign states, event, guard, invariant, reset of a transition of fautly path and normal path.
            self.s.add(Implies(
                self.faultyPath[pos] == j, self.idTransitionFaultyPath[pos] == self.labelTransition[j]))
            self.s.add(Implies(self.faultyPath[pos] == j, self.clockConstraintFaultyPath[pos] == And(
                self.transConstraints(self.parseConstraints(self.clockTransition[j]), pos, 'f'))))
            self.s.add(Implies(
                self.normalPath[pos] == j, self.idTransitionNormalPath[pos] == self.labelTransition[j]))
            self.s.add(Implies(self.normalPath[pos] == j, self.clockConstraintNormalPath[pos] == And(
                self.transConstraints(self.parseConstraints(self.clockTransition[j]), pos, 'n'))))

            for i in range(self.automaton.clockNum):
                self.s.add(Implies(
                    self.faultyPath[pos] == j, self.resetConstraintFaultyPath[i][pos] == self.resetTransition[i][j]))
                self.s.add(Implies(
                    self.normalPath[pos] == j, self.resetConstraintNormalPath[i][pos] == self.resetTransition[i][j]))

                transition = self.automaton.getTransitionAt(j)
                sourceState = transition.getSourceState()
                finalState = transition.getFinalState()

                self.s.add(Implies(self.faultyPath[pos] == j, self.sourceInvFaultyPath[i][pos] == And(
                    self.parseInv(sourceState.getInvariant(), i, pos, 'f'))))
                self.s.add(Implies(self.faultyPath[pos] == j, self.finalInvFaultyPath[i][pos] == And(
                    self.parseInv(finalState.getInvariant(), i, pos+1, 'f'))))

                self.s.add(Implies(self.normalPath[pos] == j, self.sourceInvNormalPath[i][pos] == And(
                    self.parseInv(sourceState.getInvariant(), i, pos, 'n'))))
                self.s.add(Implies(self.normalPath[pos] == j, self.finalInvNormalPath[i][pos] == And(
                    self.parseInv(finalState.getInvariant(), i, pos+1, 'n'))))

        self.s.add(self.clockConstraintFaultyPath[pos] == True)
        self.s.add(self.clockConstraintNormalPath[pos] == True)

        # clocks progress
        for j in range(self.automaton.clockNum):
            self.s.add(Implies(self.resetConstraintFaultyPath[j][pos] == True,
                       self.clockValueFaultyPath[j][pos + 1] == 0 + self.delayClockFaultyPath[pos+1]))

            self.s.add(Implies(self.resetConstraintFaultyPath[j][pos] == False, self.clockValueFaultyPath[j]
                       [pos + 1] == self.clockValueFaultyPath[j][pos] + self.delayClockFaultyPath[pos+1]))

            self.s.add(Implies(self.resetConstraintNormalPath[j][pos] == True,
                       self.clockValueNormalPath[j][pos+1] == 0 + self.delayClockNormalPath[pos+1]))

            self.s.add(Implies(self.resetConstraintNormalPath[j][pos] == False, self.clockValueNormalPath[j]
                       [pos + 1] == self.clockValueNormalPath[j][pos] + self.delayClockNormalPath[pos+1]))

            self.s.add(And(self.sourceInvFaultyPath[j][pos] ==
                       True, self.finalInvFaultyPath[j][pos] == True))

            self.s.add(And(self.sourceInvNormalPath[j][pos] ==
                       True, self.finalInvNormalPath[j][pos] == True))

        self.s.add(self.delayClockFaultyPath[pos] >= 0)
        self.s.add(self.delayClockNormalPath[pos] >= 0)

        self.s.add(self.delayClockNormalPath[pos+1] >= 0)
        self.s.add(self.delayClockFaultyPath[pos+1] >= 0)

        # global clock progress
        self.s.add(
            self.globalClockFaultyPath[pos] == self.globalClockFaultyPath[pos-1] + self.delayClockFaultyPath[pos])
        self.s.add(
            self.globalClockNormalPath[pos] == self.globalClockNormalPath[pos-1] + self.delayClockNormalPath[pos])

        # delay of nop is 0
        self.s.add(
            Implies(self.faultyPath[pos] == 0, self.delayClockFaultyPath[pos] == 0))
        self.s.add(
            Implies(self.normalPath[pos] == 0, self.delayClockNormalPath[pos] == 0))

        if pos >= 1:
            self.s.add(If(self.faultyPath[pos] == 0, self.lengthFaultyPath[pos] == self.lengthFaultyPath[pos]
                       == self.lengthFaultyPath[pos-1], self.lengthFaultyPath[pos] == self.lengthFaultyPath[pos-1] + 1))
            self.s.add(If(self.normalPath[pos] == 0, self.lengthNormalPath[pos] == self.lengthNormalPath[pos]
                       == self.lengthNormalPath[pos-1], self.lengthNormalPath[pos] == self.lengthNormalPath[pos-1] + 1))

        # synchronize
        self.s.add(And(Or(self.idTransitionFaultyPath[pos] > self.NO_OBS,
                          self.idTransitionNormalPath[pos] > self.NO_OBS), self.isObservableTransition[pos]) == self.checkSynchro[pos])
        # PREVIOUS VERSION WITH NO CONTROL ON OBSERVATION.
        # self.s.add(Or(self.idTransitionFaultyPath[pos] > self.NO_OBS,
        #           self.idTransitionNormalPath[pos] > self.NO_OBS) == self.checkSynchro[pos])
        self.s.add(Or(Not(self.checkSynchro[pos]), And(self.idTransitionFaultyPath[pos] ==
                   self.idTransitionNormalPath[pos], self.globalClockFaultyPath[pos] == self.globalClockNormalPath[pos])))

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
        # self.cptFaultOccursByThePast.append(Real("cptFaultOccurs_" + str(idx)))
        self.checkSynchro.append(Bool("checkSynchro_" + str(idx)))

        self.globalClockFaultyPath.append(Real("g_fp_" + str(idx)))
        self.globalClockNormalPath.append(Real("g_np_" + str(idx)))

        self.delayClockFaultyPath.append(Real("delay_fp_" + str(idx+1)))
        self.delayClockNormalPath.append(Real("delay_np_" + str(idx+1)))

        self.clockConstraintFaultyPath.append(
            Bool("constraint_fp_" + str(idx)))
        self.clockConstraintNormalPath.append(
            Bool("constraint_np_" + str(idx)))

        self.cptFaultOccursByThePast.append(
            Real("cptFaultOccurs_" + str(idx+1)))

        self.lengthFaultyPath.append(Int("length_fp_" + str(idx)))
        self.lengthNormalPath.append(Int("length_np_" + str(idx)))

        for i in range(self.automaton.clockNum):  # reset need next clock value
            self.clockValueFaultyPath[i].append(
                Real("clock" + str(i + 1) + "_fp_" + str(idx+1)))
            self.clockValueNormalPath[i].append(
                Real("clock" + str(i + 1) + "_np_" + str(idx+1)))

            self.resetConstraintFaultyPath[i].append(
                Int("reset" + str(i + 1) + "_fp_" + str(idx)))
            self.resetConstraintNormalPath[i].append(
                Int("reset" + str(i + 1) + "_np_" + str(idx)))

            self.sourceInvFaultyPath[i].append(
                Bool("sourceInv" + str(i + 1) + "_fp_" + str(idx)))
            self.finalInvFaultyPath[i].append(
                Bool("finalInv" + str(i + 1) + "_fp_" + str(idx)))

            self.sourceInvNormalPath[i].append(
                Bool("sourceInv" + str(i + 1) + "_np_" + str(idx)))
            self.finalInvNormalPath[i].append(
                Bool("finalInv" + str(i + 1) + "_np_" + str(idx)))

    def incBound(self):
        """
        Extend the bound allowing a new transition.
        """
        idx = len(self.faultyPath)
        assert(idx > 0)

        self.incVariableList()

        # we reduce the domain to what it is necessary
        self.s.add(self.faultyPath[idx] <= self.automaton.getNbTransition())
        self.s.add(self.normalPath[idx] <= self.automaton.getNbTransition())

        self.s.add(self.idTransitionFaultyPath[idx] <= self.maxLabelTransition)
        self.s.add(self.idTransitionNormalPath[idx] <= self.maxLabelTransition)

        # set the lastly active transition.
        self.s.add(Implies(self.faultyPath[idx] == self.NOP_TRANSITION,
                   self.lastlyActiveFaultyPath[idx] == self.lastlyActiveFaultyPath[idx-1]))
        self.s.add(Implies(self.faultyPath[idx] != self.NOP_TRANSITION,
                   self.lastlyActiveFaultyPath[idx] == self.faultyPath[idx]))
        self.s.add(Implies(self.normalPath[idx] == self.NOP_TRANSITION,
                   self.lastlyActiveNormalPath[idx] == self.lastlyActiveNormalPath[idx-1]))
        self.s.add(Implies(self.normalPath[idx] != self.NOP_TRANSITION,
                   self.lastlyActiveNormalPath[idx] == self.normalPath[idx]))

        # verify that transitions are correct regarding the label.
        for j in range(self.automaton.getNbTransition()):
            self.s.add(Implies(self.lastlyActiveFaultyPath[idx-1] == j, Or(
                [self.faultyPath[idx] == n for n in self.nextTransition[j]])))
            self.s.add(Implies(self.lastlyActiveNormalPath[idx-1] == j, Or(
                [self.normalPath[idx] == n for n in self.nextTransition[j]])))

        # no fault in the normal path.
        self.s.add(self.idTransitionNormalPath[idx] != self.FAULT)

        # delay in the normal path and faulty path >= 0
        self.s.add(self.delayClockFaultyPath[idx] >= 0)
        self.s.add(self.delayClockNormalPath[idx] >= 0)

        # we add the constraints that specify the id of the transition
        self.addConstraintOnIdTransition(idx)

        # specify if the transition is a nop
        self.s.add(self.nopFaultyPath[idx] == (
            self.faultyPath[idx] == self.NOP_TRANSITION))
        self.s.add(self.nopNormalPath[idx] == (
            self.normalPath[idx] == self.NOP_TRANSITION))

        # we want to progress
        self.s.add(
            Or(Not(self.nopFaultyPath[idx]), Not(self.nopNormalPath[idx])))

        # breaking symmetries in the nop schema
        self.s.add(Implies(self.nopFaultyPath[idx-1], Or(
            self.nopFaultyPath[idx], self.idTransitionFaultyPath[idx] > self.NO_OBS)))
        self.s.add(Implies(self.nopNormalPath[idx-1], Or(
            self.nopNormalPath[idx], self.idTransitionNormalPath[idx] > self.NO_OBS)))

        # the dynamic of the fault list of variables
        self.s.add(Or(self.faultOccursByThePast[idx-1], self.idTransitionFaultyPath[idx]
                   == self.FAULT) == self.faultOccursByThePast[idx])

        # set the counter since when the fault occurs.
        self.s.add(Implies(
            self.faultOccursByThePast[idx-1] == False, self.cptFaultOccursByThePast[idx] == 0))

        # count delta.
        self.s.add(Implies(
            self.faultOccursByThePast[idx] == False, self.cptFaultOccursByThePast[idx+1] == 0))
        self.s.add(Implies(self.faultOccursByThePast[idx] == True, self.cptFaultOccursByThePast[idx+1]
                   == self.cptFaultOccursByThePast[idx] + self.delayClockFaultyPath[idx+1]))

        # self.s.add(Implies(And(self.faultOccursByThePast[idx-2] == False, self.faultOccursByThePast[idx-1] == True), self.cptFaultOccursByThePast[idx] == self.cptFaultOccursByThePast[idx-1] + self.delayClockFaultyPath[idx] + self.delayClockFaultyPath[idx + 1]))
        # self.s.add(Implies(And(self.faultOccursByThePast[idx-2] == True, self.faultOccursByThePast[idx-1] == True), self.cptFaultOccursByThePast[idx] == self.cptFaultOccursByThePast[idx-1]  + self.delayClockFaultyPath[idx + 1]))

    def printAutomatonInfo(self):
        """
        Print information about the given automaton
        """
        print("Information ...")
        print("automata:")

        print(self.automaton)

        print("next transition:")
        for i in range(len(self.nextTransition)):
            print(i, ':', self.nextTransition[i])

        print("BOUND:", self.BOUND)
        print("DELTA:", self.DELTA)
        print("delta:", self.delta)

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
        # delta = int(model.evaluate(self.delta).as_long())
        bound = int(model.evaluate(self.bound).as_long())
        # k = int(model.evaluate(self.k).as_long())
        # assert(delta == (bound - k - 1))

        previous = None
        for i in range(len(self.faultyPath)):
            v = int(model.evaluate(self.faultyPath[i]).as_long())
            if i > 0:
                lv = int(model.evaluate(
                    self.lastlyActiveFaultyPath[i-1]).as_long())
            id = int(model.evaluate(self.idTransitionFaultyPath[i]).as_long())
            nop = model.evaluate(self.nopFaultyPath[i])
            assert(id == 0 or self.automaton.getTransitionAt(
                v).getFinalState().getId() == id)

            assert(nop or v != 0)
            if previous != None:
                assert(
                    nop or self.automaton.getTransitionAt(previous).getFinalState() == self.automaton.getTransitionAt(v).getSourceState())
                print(lv, previous)
                assert(lv == previous)

            if not nop:
                previous = v

        previous = None
        for i in range(len(self.normalPath)):
            v = int(model.evaluate(self.normalPath[i]).as_long())
            if i > 0:
                lv = int(model.evaluate(
                    self.lastlyActiveNormalPath[i-1]).as_long())
            id = int(model.evaluate(self.idTransitionNormalPath[i]).as_long())
            nop = model.evaluate(self.nopNormalPath[i])
            assert(id == 0 or self.automaton.getTransitionAt(
                v).getFinalState().getId() == id)

            assert(nop or v != 0)
            if previous != None:
                assert(
                    nop or self.automaton.getTransitionAt(previous).getFinalState() == self.automaton.getTransitionAt(v).getSourceState())
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
            print('{:-6}'.format(int(model.evaluate(x).as_long())), end=" ")
        print()

    def printOneRealArray(self, model, array, cpt):
        """
        Print a list of z3 variables.

        :param model: the model we want to check.
        :type model: a z3 model.
        :param array: the list of z3 variables we want to print out.
        :param cpt: the length of the path
        :type model: list of integer z3 variables.
        """
        print([model[array[i]] for i in range(cpt)])

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
            print('{:-6}'.format(id), end=" ")
        print()

    def printModel(self, model, cpt):
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
        # self.printOneIntArray(model, self.cptFaultOccursByThePast)
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
        print("globalClockFaultyPath")
        self.printOneRealArray(model, self.globalClockFaultyPath, cpt)
        print("globalClockNormalPath")
        self.printOneRealArray(model, self.globalClockNormalPath, cpt)

        print("delta")
        self.printOneRealArray(model, self.cptFaultOccursByThePast, cpt+1)
        print("delayNP")
        self.printOneRealArray(model, self.delayClockNormalPath, cpt+1)
        print("delayFP")
        self.printOneRealArray(model, self.delayClockFaultyPath, cpt+1)

        print()

    def parseConstraints(self, constraint_original):
        """
        Split the entire inequality into a single inequality. Then z3 slover chould process.
        ex:  [['10>=c1>=0', '5>c2>=0']] to ['10>=c1','c1>=0','5>c2','c2>=0']

        :param: constraint_original: the original clock constraint form a transition(transtion[i][3]).
        :type:  a list.
        :return: con
        :type: a list
        """
        con = []
        constraint = constraint_original.copy()
        while len(constraint) != 0:
            clocknum = constraint[0].split("c")[1].split(">")[0]
            clock = 'c' + str(clocknum)
            j = constraint[0].split(clock)
            for jj in j:
                if jj != "":
                    jjj = list(jj)
                    if jjj[0] == ">":
                        item = clock + jj
                    else:
                        item = jj + clock
                else:
                    item = constraint[0]
                    continue

                con.append(item)
                item = ""
            constraint.remove(constraint[0])
        return con

    def transConstraints(self, constraint_single, idx, property):
        """
         This used to transform string constraints to boolstring constraints
         This step is after paserConstraints. In paserConstraints, constraints are string type.
         z3 could not process directly, only translate to boolstring, z3 could process.

         :param: constraint_single: the clock Constraint we want to translate.
                idx : index of the transition in generating, decide the clock name
         :type: constraint_singlt: a list.
         :return: ex
         :type: a list store literals(inequality) then z3 could directly process.

        """

        # constraint =str(constaintlist[0])
        clocklist = ["c" + str(i + 1) for i in range(self.automaton.clockNum)]
        ex = []
        for i in constraint_single:
            flag = 0
            # ii = list(i)
            num = i.split("=")
            if list(num[0])[0] == "c":
                if len(num) == 1:
                    flag = 1
                    nummber = num[0].split(">")[1]
                else:
                    flag = 2
                    nummber = num[1]

                clock = num[0].split(">")[0]
            else:
                if len(num) == 1:
                    flag = 3
                    nummber = num[0].split(">")[0]
                    clock = num[0].split(">")[1]
                else:
                    flag = 4
                    nummber = num[0].split(">")[0]

                    clock = num[1]
            nummber = float(nummber)

            for j in range(len(clocklist)):
                if clock == clocklist[j] and property == "f":
                    if flag == 1:
                        item = self.clockValueFaultyPath[j][idx] > nummber
                    if flag == 2:
                        item = self.clockValueFaultyPath[j][idx] >= nummber
                    if flag == 3:
                        item = self.clockValueFaultyPath[j][idx] < nummber
                    if flag == 4:
                        item = self.clockValueFaultyPath[j][idx] <= nummber
                elif clock == clocklist[j] and property == "n":
                    if flag == 1:
                        item = self.clockValueNormalPath[j][idx] > nummber
                    if flag == 2:
                        item = self.clockValueNormalPath[j][idx] >= nummber
                    if flag == 3:
                        item = self.clockValueNormalPath[j][idx] < nummber
                    if flag == 4:
                        item = self.clockValueNormalPath[j][idx] <= nummber
                continue

            ex.append(item)

        # self.s.add([And(x) for x in ex])
        return ex

    def transReset(self, resetConstraint):
        """
         translate reset information(string) to reset(list): transtionList[i][4] to reset(list).
         reset[] initialized by reset[0,0,0...], len(reset) == clocknum. 0 in not reset, otherwise is reset.
         the value of reset[0] means whether clock c1 is reset.

         :param: resetConstraint: the resetConstraint which need to translate.
         :type: resetConstraint: a string.
         :return: reset
         :type: a list

        """
        resetList = resetConstraint.split(";")
        reset = []
        for i in range(self.automaton.clockNum):
            reset.append(0)
        for element in resetList:
            if element != '0':  # maybe bug
                clockIndex = int(element.split("c")[1])
                reset[clockIndex - 1] = 1
        return reset

    def parseInv(self, invariant, clock, pos, property):
        """
        This used to transform string invariant to boolstring constraints of corresponding clocks.

        :param invariant: the invariant we want to translate.
        :param clock: the index of clock the invariant corresponding to.
        :param pos : index of the transition of generating.
        :param property: faulty path or normal path.

        :return result: a boolstring or true if no invaraint.
        """

        result = True
        if invariant == 1:
            result = True
        else:
            invariantList = invariant.split(';')
            for i in invariantList:
                clockindex = i.split('c')[1]
                if clockindex == str(clock+1):
                    number = int(i.split('>')[0])
                    if property == 'f':
                        result = self.clockValueFaultyPath[clock][pos] <= number
                    elif property == 'n':
                        result = self.clockValueNormalPath[clock][pos] <= number
                    break
        return result

    def run(self):
        """
        Run the main program.
        """
        # run in normal mode

        assumD = Bool("d" + str(self.idxAssum))
        self.s.add(Implies(assumD, self.delta == self.DELTA))

        for i in range(self.automaton.getNbTransition()):
            self.s.add(
                self.labelTransition[i] == self.automaton.getTransitionAt(i).getEventId())

        cpt = 1
        while cpt <= self.BOUND:
            # while cpt < (2 * self.BOUND)

            cpt += 1
            self.incBound()

            # assumption:
            self.idxAssum += 1
            assumB = Bool("b" + str(self.idxAssum))    # fix the bound
            # ensure that we have enough real transition at the end
            assumF = Bool("f" + str(self.idxAssum))

            self.s.add(Implies(assumB, self.bound == len(self.faultyPath)))

            self.s.add(
                Implies(assumF, self.cptFaultOccursByThePast[-1] == self.DELTA))
            # self.s.add(Implies(assumF, self.cptFaultOccursByThePast[-1]> self.delta))

            assumFO = Bool("fo" + str(self.idxAssum))
            self.s.add(Implies(assumFO, self.faultOccursByThePast[-1] == True))

            # if BOUND is real, except nop, this part should be used.
            # self.s.add(self.lengthFaultyPath[-1] <= self.BOUND)
            # self.s.add(self.lengthNormalPath[-1] <= self.BOUND)

            tmp = list(self.isObservableTransition)
            # for i in range(len(tmp)):
            #     tmp[i] = Not(tmp[i])
            # tmp[1] = Not(tmp[1])
            # tmp[2] = Not(tmp[2])
            # tmp[3] = Not(tmp[3])

            # listAssum = [assumB, assumF, assumFO] + [l for l in self.isObservableTransition]
            listAssum = [assumB, assumF, assumFO] + tmp

            res = self.s.check(assumD, *listAssum)

            if res == sat:
                print("sat")
                # print(self.s.model())
                m = self.s.model()
                # self.checkModel(m)
                self.printModel(m, cpt)

                # print(self.s.model()[self.cptFaultOccursByThePast[3]])

                # print(self.s.model())
                return
            else:
                print("Increase the bound:", len(self.faultyPath) + 1)

        print(self.s.unsat_core())

        print("The problem is UNSAT")


# the automata.
assert(len(sys.argv) == 2)
# z3Model = Z3Model(sys.argv[1])
z3Model = Z3Model()
z3Model.printAutomatonInfo()
start = time.time()
z3Model.run()
end = time.time()
print(str(end-start))
