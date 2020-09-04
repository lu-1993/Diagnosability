
'''
/**
 * The goal is to define semantics of some propositional variable.
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
 *
 */
'''

class observableEvent():
    # This class to define semantic to verify whether a given event (integer) is an observable event.
    # <def>observableEventSemantic</def> if yes, return true, otherwise, return false.

    # :@param an <code>observableEventSet</code> is a set storing all events
    # :@return a formula representing this semantic

    def __init__(self,observableEventSet):
        self.observableEventSet = observableEventSet

    def observableEventSemantic(self):
        # :@param
        note = ";function to verify whether a given event (integer) is an observable event\n\n"
        strDefine = "(define-fun obs ((o Int)) Bool\n( if (and ( >= o 1)( <= o "
        observableNum = str(len(self.observableEventSet))
        strSemantic = "))\ntrue\nfalse))\n\n"
        strEventSemantic = note + strDefine + observableNum + strSemantic
        return strEventSemantic

class existFault():
    # This class to define semantic to verify whether a given event is a fault.
    # <def>existFaultSemantic</def> if yes, return true, otherwise, return false.
    # In our algorithm, we check all events associated in a path, if any one event is a fault,
    # then this path is faulty path.


    # :@param an <code>normalEventSet</code> is a set storing all normal events
    # :@return a formula representing this semantic

    def __init__(self,normalEventSet):
        self.normalEventSet = normalEventSet

    def existFaultSemantic(self):
        note = ";function to check whether a given event on the faulty path \n\n"
        strDefine = "(define-fun existF((fau Int)) Bool\n( if (> (eventFault fau) "
        normalEventNum = str(len(self.normalEventSet))
        strSemantic = ")\ntrue\nfalse))\n\n"
        strExistFaultSemantic = note + strDefine + normalEventNum + strSemantic
        return strExistFaultSemantic

class notFault():
    # This class to define semantic to verify whether a given event is a normal event.
    # <def>notFaultSnmantic</def> if yes, return true, otherwise, return false.
    # In our algorithm, we check all events associated in a path, if all events are normal,
    # then this path is normal path.

    # :@param an <code>normalEventSet</code> is a set storing all normal events
    # :@return a formula representing this semantic

    def __init__(self,normalEventSet):
        self.normalEventSet = normalEventSet

    def notFaultSnmantic(self):
        strDefine = "(define-fun notF((nor Int)) Bool\n( if (and ( >= (event nor) 1)(<= (event nor) "
        normalEventNum = str(len(self.normalEventSet))
        strSemantic = "))\ntrue\nfalse))\n\n"
        strNotFaultSemantic = strDefine + normalEventNum + strSemantic
        return strNotFaultSemantic



















