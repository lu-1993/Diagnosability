
class Transition:
    """
    Class to store transition information.
    """
    uniq_id = 0

    def __init__(self, source, target, event, guard, reset):
        """
        Constructor.
        """
        self.id = Transition.uniq_id
        Transition.uniq_id = Transition.uniq_id + 1

        self.source = source
        self.target = target
        self.event = event
        self.guard = guard
        self.reset = reset

    def __str__(self):
        """
        ToString method
        """
        return "*********************\nTransition id = " + str(self.id) + ":\n" + str(self.source) + " -> " + str(self.target) + "\nevent = " + str(self.event) + "\nguard = " + str(self.guard) + "\nreset = " + str(self.reset)

    def getFinalState(self):
        """
        Getter.
        """
        return self.target

    def getSourceState(self):
        """
        Getter.
        """
        return self.source

    def getResetList(self):
        """
        Getter.
        """
        return self.reset

    def getGuard(self):
        """
        Getter.
        """
        return self.guard

    def getEventId(self):
        """
        Getter.
        """
        return self.event
