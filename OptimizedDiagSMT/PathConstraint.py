'''
/**
 * The goal is to generate formulas representing path constraints.
 * In our algorithm, there are two path,
 * the variables equipped with a "fault" or "f" are associated to the faulty path,
 * the variables without a "Fault" are associated to the normal path.

 * @author Lulu HE
 * @Email helulu@lri.fr
 *
 */
 '''
class Init():
    # This class to generate formulas indicates system initialization.

    def __init__(self):
        pass

    def InitEvent(self):
        # declare event <code>event</code> in normal path.
        # declare event <code>eventFault</code> in faulty path.

        note = ";define event (events of normal path) and eventFault (events of faulty path) and initialization\n"
        DeclareEventNormal = "(declare-fun event (Int) Int)\n"
        DeclareEventFault = "(declare-fun eventFault (Int) Int)\n"
        InitEventNormal = "(assert (= (event -1) 0))\n"
        InitEventFault = "(assert (= (eventFault -1) 0))\n"
        InitEventStr = note + DeclareEventNormal + DeclareEventFault + InitEventNormal + InitEventFault
        return InitEventStr

    def InitState(self):
        # declare state <code>loc</code> in normal path.
        # declare state <code>locFault</code> in faulty path.

        note = ";define loc (states of normal path) and locFault (states of faulty path) and initialization (both begin from the state 1)\n"
        DeclareLocNormal = "(declare-fun loc (Int) Int)\n"
        DeclareLocFault = "(declare-fun locFault (Int) Int)\n"
        InitLocNormal = "(assert (= (loc 0) 1))\n"
        InitLocFault = "(assert (= (locFault 0) 1))\n"
        InitLocStr = note + DeclareLocNormal + DeclareLocFault + InitLocNormal + InitLocFault
        return InitLocStr

    def InitLength(self):
        # declare length <code>ln</code> of normal path.
        # declare length <code>lf</code> of faulty path.
        Str = "(declare-const lf Int)\n(declare-const ln Int)\n"
        return Str


class ComputerK():
    # This class is to generate formulas indicating the process to computer k value of faulty path.

    # :@param <code>normalEventSet</code> stores all normal events
    # :@return smt formulas representing the process to computer k.

    def __init__(self,normalEventSet):
        self.normalEventSet = normalEventSet


    def note(self):
        NoteStr = ";some functions to computer k-value on the specific transition (k represents the number of steps after the fault)\n"
        return NoteStr


    def iFault(self):
        # function to set flag representing whether an event in step i is a fault in faulty path,
        # if yes, return 1, otherwise, return 0.
        DeclareIFault =  "(define-fun ifault((fau Int)) Int\n"
        MainIFault = "( if (> (eventFault fau) " + str(len(self.normalEventSet)) + ")\n"
        ResultIFault  = "1\n0))\n\n"
        InitIFault = "(assert (=(ifault -1)0))\n\n"
        IFaultStr = DeclareIFault + MainIFault + ResultIFault + InitIFault
        return IFaultStr


    def IsFault(self):
        # function to check weather a fault occur before step i.
        DecalreIsFault = "(declare-fun isfault (Int) Int)\n"
        InitIsFault = "(assert (=(isfault -1)0))\n"
        IsFaultStr = DecalreIsFault + InitIsFault
        return IsFaultStr


    def ComputerIsFault(self):
        # function to check weather a fault occur before step i.
        Declare = "(define-fun midk ((i Int)) Bool\n"
        Main = "( if (or (= (ifault i) 1)(= (isfault (- i 1)) 1))\n"
        Result  = "(= (isfault i) 1)\n(= (isfault i) 0)))\n"
        Str = Declare + Main + Result
        return Str

    def KValue(self):
        # function to declare k.
        Declare =  "(declare-fun k (Int) Int)\n"
        Init  = "(assert (= (k -1) -1))\n\n"
        Str = Declare + Init
        return Str

    def ComputerK(self):
        # function to computer k in each transition.
        Declare = "(define-fun compk ((i Int)) Bool\n"
        Main = "(if (=(isfault i)0)\n"
        Result = "(=(k i) -1)\n(= (k i) (+(k (- i 1))1))))\n\n"
        Str = Declare + Main + Result
        return Str

class LengthPath():
    # This class to generate smt formulas representing the length of normal path <code>ln</code>
    # and the length of faulty path <code>lf</code>
    def __init__(self):
        pass

    def note(self):
        NoteStr = ";declare two const. lf/ln: length fo faulty/normal path\n"
        return NoteStr

    def NormalPathLength(self):
        Declare = "(declare-const ln Int)\n"
        Str = Declare
        return Str

    def FaultyPathLength(self):
        Declare = "(declare-const lf Int)\n"
        Str = Declare
        return Str

class Array():
    # This class to generate smt formulas representing the array to store observable events of normal path <code>obsn</code>
    # and the array to store observable events of faulty path <code>obsf</code>

    def __init__(self):
        pass

    def note(self):
        NoteStr = ";declare two array. obsn/obsf: array to store all observable events on the normal/faulty path;\n"
        return NoteStr

    def NormalArray(self):
        Declare = "(declare-const obsn (Array Int Int))\n"
        Index = "(declare-fun count (Int) Int)\n(assert (= (count 0) 0))\n"
        Init = "(assert ( = (count -1) -1))\n(assert ( = (store obsn -1 0) obsn ))\n\n"
        Str = Declare + Index + Init
        return Str

    def FaultyArray(self):
        Declare = "(declare-const obsf (Array Int Int))\n"
        Index = "(declare-fun countf (Int) Int)\n(assert (= (countf 0) 0))\n"
        Init = "(assert ( = (countf -1) -1))\n(assert ( = (store obsf -1 0) obsf ))\n\n"


        Str = Declare + Index + Init
        return Str

class CreatePath():
    # This class to generate smt formulas ensuring that construct a faulty path of length <code>lf</code>
    # and a normal path of length <code>lf</code>
    # the <code>first</code> of a <code>datatype</code> is source state of a transition,
    # the <code>second</code> of <code>datatype</code> is destination state of a transition,
    # the <code>third</code> of <code>datatype</code> is destination state of a transition.

    def __init__(self,modelsmt,bound):
        self.bound = bound
        self.NoteFaultyPath = ";construct faulty path of length " +str(self.bound + 1)+"\n"
        self.NothNormalPath = ";construct normal path of length " +str(self.bound + 1)+"\n"
        self.notelocf = "\n;construct faulty path\n"
        self.TransitionsSet = open(modelsmt,"r").readlines()


    def CreateFaultyPath(self):

        Transition = ""
        strlocftotal = ""
        linklocf = "(or"

        for k in range(1, len(self.TransitionsSet) + 1):

            linkAnd = "(and "
            BeginState = "(= (first (trS " + str(k) + ")) (locFault " + str(self.bound) + "))"
            Event = "(= (eventFault " + str(self.bound) + ") (third (trS " + str(k) + ")))"
            EndState = "(= (locFault  " + str(self.bound + 1) + ") (second (trS " + str(k) + "))))"
            Transition = Transition + linkAnd + BeginState + Event + EndState
            strlocftotal  = strlocftotal + Transition
            Transition = ""

        LineBreak = ")\n"
        strTransition = linklocf + strlocftotal + LineBreak

        TransitionsTotal = self.NoteFaultyPath + strTransition


        return TransitionsTotal

    def CreateNormalPath(self):
        Transition = ""
        strloctotal = ""
        linkloc = "(or"

        for k in range(1, len(self.TransitionsSet) + 1):
            linkAnd = "(and "
            BeginState = "(= (first (trS " + str(k) + ")) (loc " + str(self.bound) + "))"
            Event = "(= (event " + str(self.bound) + ") (third (trS " + str(k) + ")))"
            EndState = "(= (loc " + str(self.bound + 1) + ") (second (trS " + str(k) + "))))"
            Transition = Transition + linkAnd + BeginState + Event + EndState
            strloctotal = strloctotal + Transition
            Transition = ""

        LineBreak = ")\n"
        strTransition = linkloc + strloctotal + LineBreak


        TransitionsTotal = self.NothNormalPath + strTransition

        return TransitionsTotal




class FaultyPathConstraint():
    # This class to generate smt formulas ensuring that faulty path exists.
    # <def>AtLeastOneFault</def> ensure at least one fault occurring in faulty path.
    # <def>VerifyK</def> ensure in any transition of faulty path, the k is satisfied.
    # <def>ObservableEventArray</def> ensure all observable events of faulty path are stored in array <code>obsf</code>


    def __init__(self,boundCurrent,k,bound):
        self.bound = boundCurrent
        self.BoundValue = bound
        self.k = k
        self.NoteExistF = ";check that at least one fault occur on the faulty path\n"
        self.NoteComputerK =";computer k value in each step\n"
        self.NoteGetLength =";lenght of the faulty path\n"
        self.NoteArray = ";array to store all observable events of the faulty path\n"


    # declare the name of every transition
    # declare the name of existF clause
    def InitFlag(self):
        DeclareClause = "(declare-fun c0 () Bool)\n"
        for i in range(0,self.BoundValue+1):
            DeclareClause = DeclareClause + "(declare-fun b" + str(i) + " () Bool)\n"
        return DeclareClause

    def AtLeastOneFault(self):
        ExistFStr = "(assert (=> c0 (= (k " + str(self.BoundValue-1) + ")" + str(self.k) + ")))\n"
        return ExistFStr

    def ComputerK(self):

        computerK = "(compk " +str(self.bound)+")\n(midk " +str(self.bound)+")\n"
        return computerK

    def ObservableEventArray(self):

        obsf = ""
        linkobsf = "(and"


        obsf = obsf + "(ite (and (=(obs (eventFault " + str(self.bound) + ")) true)(not(=(eventFault "+ str(self.bound) + ")(select obsf ( - (countf " +str(self.bound) + ") 1 )))))(and (= (countf " + str(self.bound + 1) + ") (+ (countf " + str(self.bound) + ") 1))(= (store obsf (countf " + str(self.bound) + ") (eventFault " + str(self.bound) + ")) obsf)) (= (countf " + str(self.bound + 1) + ")(countf " + str(self.bound) + ")))"
        LineBreak = ")\n"
        obsf = self.NoteArray + linkobsf + obsf + LineBreak

        return obsf

    def VerifyK(self):

        # the k value in this step
        k = "(k " + str(self.bound) + ")"

        Continue = " b" + str(self.bound + 1) + "\n"
        Stop = "(ite (and (=" + k + str(self.k)+  ")(not b"+ str(self.bound+1) + " ))\n(= lf "+str(self.bound+1)+")\n false))\n"
        Verify = "(ite (< " + k + str(self.k) + ")\n" + Continue + Stop

        return Verify

    def SatK(self):
        # This function to ensure in faulty path, k is satisfied in anyone transitions.
        s = "(assert (or "
        a = ""
        for i in range(0,self.BoundValue):
            a = a + "(=( k " + str(i) + ")" + str(self.k) + ")"

        s = s + a + "))\n"

        return s






class NormalPathConstraint():
    # This class to generate smt formulas ensuring that normal path exist.
    # <def>NotFaultOccur</def> ensure no fault occurring in normal path.
    # <def>ObservableEventArray</def> ensure all observable events of normal path are stored in array <code>obsn</code>
    # <def>GetNormalPathLength</def> ensure that <code>ln</code> is the length of the normal path.
    #
    # <def>Equivalent</def> ensure that the observable events in normal path stored in <code>obsn</code> is the same
    # as faulty path stored in <code>obsf</code>
    #
    # <def>CheckSat<def> ensure if the obsn equivalent obsf possibly, the tuidong process in next transitions,
    # it's incremental way in smt, if not, the process end, and return result.
    #
    # declare flag <code>a_i</code> of every transition on normal path.

    def __init__(self,boundCurrent,k,Bound):
        self.bound = boundCurrent
        self.k = k
        self.NoteNotF = ";;check that all transitions are labeled normal events on the normal path\n"
        self.NoteGetLength =";lenght of the normal path\n"
        self.NoteArray = ";array to store all observable events of the normal path\n"
        self.BoundValue = Bound
        #self.lf = lf

    def InitFlag(self):
        DeclareClause = ""
        for i in range(0,self.BoundValue+1):
            DeclareClause = DeclareClause + "(declare-fun a" + str(i) + " () Bool)\n"
        return DeclareClause


    def NotFaultOccur(self):

        strnotF = "(notF " + str(self.bound) + ")\n"
        return strnotF


    def ObservableEventArray(self):

        obsn = ""
        linkobsn = "(and"



        obsn = obsn + "(ite (and (=(obs (event " + str(self.bound) + ")) true)(not(=(event "+ str(self.bound) + ")(select obsn ( - (count " +str(self.bound) + ") 1 )))))(and (= (count " + str(self.bound + 1) + ") (+ (count " + str(self.bound) + ") 1))(= (store obsn (count " + str(self.bound) + ") (event " + str(self.bound) + ")) obsn)) (= (count " + str(self.bound + 1) + ")(count " + str(self.bound) + ")))"
        LineBreak = ")\n"
        obsn = self.NoteArray + linkobsn + obsn + LineBreak

        return obsn

    def GetNormalPathLength(self):
        ln = "(= ln " + str(self.bound) + ")\n"
        return ln

    def Equivalent(self):

        Str = "(= obsn obsf)\n"
        return Str

    def TransitionVeirfy(self):
        #notF = "(notF " + str(self.bound) + ")\n"
        #NormalLenght = "(= ln "+ str(self.bound + 1) +")"
        #NoContinue = "(not a" + str(self.bound + 1) + ")\n"
        ArrayNumLessThanFaultyPath = "( < (count "+str(self.bound+1)+")(countf lf))"
        ArrayNumEquivlence = "( = (count "+str(self.bound+1)+")(countf lf))"
        Continue = "(> ln "+ str(self.bound + 1) +")\n"

        Continue = "(ite"+ "(and" + ArrayNumLessThanFaultyPath +")\n" + Continue
        SatAndStop = "(and (= ln " + str(self.bound + 1) + ") (not a"+ str(self.bound+1) +"))\n"
        Stop = "(ite"+ "(and" + ArrayNumEquivlence + ")\n" + SatAndStop + 'false))\n'


        Veirfy = Continue + Stop

        return Veirfy






































































