'''
/**
 * The goal is to generate the clauses to verify the existence of a critical pair with different length.
 * Ensure the existence of a faulty path, check faulty path with length lf in range(k,bound).
 *
 *
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
**/
'''

class CheckSat:
    def __init__(self,kvalue,ln,lf):

        self.kvalue = kvalue
        self.ln = ln
        self.lf = lf


    # use push and pop to achieve incremental
    def check(self):
        push = "(push)\n"
        pop = "(pop)\n"

        # assertion check whether the current k value is equal to the given k value
        # assertion = "(assert (=> c0 (= (k " + str(self.lf) + ") " + str(self.kvalue) + ")))\n"

        assertion = "(assert (=> c0 (and (= (k " + str(self.lf) + ") " + str(self.kvalue) + ")(= lf "+str(self.lf + 1)+"))))\n"





        checksat = "(check-sat c0 "

        # faultypath is currently faulty path
        faultypath = ""
        for i in range(0,self.lf+1):
            faultypath = faultypath + "b" + str(i) + " "

        # normalpath is currently normal path
        normalpath = ""
        for i in range(0,self.ln):
            normalpath = normalpath + "a" + str(i) + " "

        # assertion check whether the faultypath and the normalpath could be a critical pair
        condition = checksat + faultypath + normalpath + ")\n"

        note = "(echo \"" + faultypath + normalpath + "\")\n"


        #----------------------------# get-value #----------------------------#

        # acquire the faulty path sequence and the normal path sequence.


        get = ("(get-value (")

        loc = "(loc 0)"
        for i in range(0, self.ln):
            loc = loc + "(loc " + str(i + 1) + ")"

        LocSequence = loc + "))\n"  #LocSequence is state sequence of normal path

        event = "(event 0)"
        for i in range(0, self.ln - 1):
            event = event + "(event " + str(i + 1) + ")"

        EventSequence = event + "))\n"  #EventSequence is event sequence of normal path

        # ln is the length of normal path
        length = "ln))\n"

        getLoc = get + LocSequence
        getEvent = get + EventSequence
        getLength = get + length

        GetNormalPath = getLength + getLoc + getEvent


        locf = "(locFault 0)"
        for i in range(0, self.lf+1):
            locf = locf + "(locFault " + str(i + 1) + ")"

        LocfSequence = locf + "))\n" #LocfSequence is state sequence of normal path

        eventf = "(eventFault 0)"
        for i in range(0, self.lf):
            eventf = eventf + "(eventFault " + str(i + 1) + ")"

        EventfSequence = eventf + "))\n"  #EventfSequence is event sequence of normal path

        # lf is the length of faulty path
        lengthf = "lf))\n"

        getLocf = get + LocfSequence
        getEventf = get + EventfSequence
        getLengthf = get + lengthf

        information = "(get-info :all-statistics)\n"

        GetFaultyPath = getLengthf + getLocf + getEventf

        checksat = push + assertion + condition + note + GetFaultyPath + GetNormalPath + information + pop

        return  checksat













