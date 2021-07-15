"""
Class Automaton.
"""

from transition import Transition
from state import State


class Automaton:
    """
    Class to store the automaton.
    """

    def __init__(self, initialStateId, clockNum):
        """
        Constructor.
        """
        self.mapState = {}
        self.transitionList = []
        self.initialStateId = initialStateId
        self.maxLabel = -1
        self.clockNum = clockNum

        self.addState(-1, 1)
        self.appendTransition(
            -1, -1, 0, ['c' + str(i+1) + ">=0" for i in range(clockNum)], [])

    def __str__(self):
        """
        toString.
        """
        assert(self.initialStateId in self.mapState)

        ret = "Initial State = " + \
            str(self.mapState[self.initialStateId]) + "\n"
        for t in self.transitionList:
            ret += str(t) + "\n"
        return ret

    def appendTransition(self, sourceId, finalId, event, guard, resetList):
        """
        Add a transition to the automaton.
        """
        assert(sourceId in self.mapState)
        assert(finalId in self.mapState)

        self.transitionList.append(Transition(
            self.mapState[sourceId], self.mapState[finalId], event, guard, resetList))

    def getState(self, stateId):
        """
        Getter.
        """
        return self.mapState[stateId]

    def addState(self, stateId, invariant):
        """
        Add a new state.
        """
        if stateId > self.maxLabel:
            self.maxLabel = stateId

        if stateId not in self.mapState:
            self.mapState[stateId] = State(stateId, invariant)

    def getTransitionAt(self, idx):
        """
        Getter.
        """
        assert(idx >= 0 and idx < len(self.transitionList))
        return self.transitionList[idx]

    def getNbTransition(self):
        """
        Getter.
        """
        return len(self.transitionList)

    def getTransitionList(self):
        """
        Getter.
        """
        return self.transitionList

    def getMaxStateLabel(self):
        """
        Getter.
        """
        return self.maxLabel

    def getClockNum(self):
        """
        Getter.
        """
        return self.clockNum

    def getInitialState(self):
        """
        Getter.
        """
        return self.mapState[self.initialStateId]
