'''
/**
* The goal is to read original model from file <code>model.txt<code/>
* and get k and bound value from parameter line(first line)
*
* Generate formulas corresponding to transitions of model (other lines) of "model.txt"
*
* @author Lulu HE
* @Email helulu@lri.fr
**/

'''

class InputGet():

    # This class acquires the model from file <code>modeltxt</code>
    # Get parameter line of model.
    # Get transitions of model.


    def __init__(self,modeltxt):
        file = open(modeltxt,"r")
        self.parameter = file.readline()
        self.model = file.read()
        #file.close()


class InitModel():

    # This class is to initialize smt program.
    # Setting unsat mode. <def>InitSet</def>
    # Get parameter line of model.
    # Get transitions of model.

    def __init__(self):
        pass

    def InitSet(self):
        # select unsat mode of smt solver
        SetUnsatCoreStr = "(set-option :produce-unsat-cores true)\n\n"
        return SetUnsatCoreStr

    def DecalreTransitionsDatetpyes(self):
        # declare structure to store transitions of model
        note = (";declare data structure to store transitions\n\n")
        AbstractTranstionsStr = "(declare-fun trS (Int) (Pair Int))\n"
        DeclareTransitionsStr = note + ("(declare-datatypes (T1) ((Pair (mk-pair (first T1) (second T1) (third T1)))))\n\n") + AbstractTranstionsStr
        return DeclareTransitionsStr



class TransformTransitions():
    # this class is to generate smt formulas corresponding to the transitions of model.
    # the <code>first</code> of a <code>datatype</code> is source state of a transition,
    # the <code>second</code> of <code>datatype</code> is destination state of a transition,
    # the <code>third</code> of <code>datatype</code> is event of a transition.

    # @:param purely number file which stores transitions of model <code>modelsmt</code>
    # @:return a smt formula representing all transitions of model. <code>TransformTransition</code>

    def __init__(self, modelsmt):
        self.transitions = modelsmt

    def TransformTransition(self):
        file = open(self.transitions, "r")
        transitionSet = file.readlines()
        TransitionsNumber = len(transitionSet)
        TransitionsStr = ";read all transitions of systems (finite automata) from modelsmt.txt\n\n"

        for i in range(1, TransitionsNumber + 1):
            line = transitionSet[i - 1].split(' ')
            declare = "(declare-const p" + str(i) + "(Pair Int))\n"
            transition = "(assert (and (= (first p" + str(i) + ") " + line[0] + ")(= (second p" + str(i) + ") " + line[
                1] + ")(= (third p" + str(i) + ") " + line[2] + ")(= (trS " + str(i) + ") p" + str(i) + ")))\n"
            TransitionsStr = declare + TransitionsStr + transition
        return TransitionsStr









