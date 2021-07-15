"""
Class state.
"""


class State:
    """
    Class to represent a state.
    """

    def __init__(self, id_state, invariant):
        """
            Constructor.
        """
        self.id_state = id_state
        self.invariant = invariant

    def __str__(self):
        """
        toString.
        """
        return str(self.id_state) + "(" + str(self.invariant) + ")"

    def getInvariant(self):
        """
        Getter.
        """
        return self.invariant

    def getId(self):
        """
        Getter.
        """
        return self.id_state
