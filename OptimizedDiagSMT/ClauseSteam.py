'''
/**
 * The goal is to accept a flow of clauses.
 * The resulting CNF then be solved or stored in
 * an external file <code>model.smt</code>.
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
**/
'''

class LinkClause():
    # This class accepts different path assertions
    # use disjunction way or conjunction way to link them.

    # @:param a list stores different assertions
    # @:return a CNF string <def>Conjunction</def>
    # @:return a DNF string <def>Disjunction</def>

    def __init__(self,Path):
        self.Path = Path

    def Conjunction(self):
        ConjunctionStr = "(and \n"
        for i in range(0,len(self.Path)):
            ConjunctionStr = ConjunctionStr + self.Path[i]

        Str = ConjunctionStr + ")\n"

        return Str

    def Disjunction(self):
        DisjunctionStr = "(or \n"
        for i in range(0,len(self.Path)):
            DisjunctionStr = DisjunctionStr + self.Path[i]

        Str = DisjunctionStr + ")\n"

        return Str


class Assert():
    # This class makes Clause into assertions.

    # @param: a string that is Clause.
    # @return: a string that is assertion.

    def __init__(self,Clause):
        self.Clause = Clause

    def Assert(self):
        Str =  "(assert " + self.Clause +")\n"
        return Str


class NamedClause():
    # This class gives Clause a name.

    # @param: Clause without name.
    # @return: Clause without name .

    def __init__(self,bound,Clause):
        self.bound = bound
        self.Clause = Clause

    def NamedNormalTransition(self):
        Str = "(=> a" + str(self.bound)+ " " + self.Clause + ")\n"
        return Str

    def NamedFaultyTransition(self):
        Str = "(=> b" + str(self.bound) + " " + self.Clause + ")\n"
        return Str


class GenerateSMT():
    # This class writes assertion to smt file.

    # @param: a string that is Clause
    # @return: an external smt format file. <code>model.smt</code>

    def __init__(self,filename,Clause):
        self.file = filename
        self.Clause = Clause

    def write(self):
        file  = open(self.file,"a")
        file.write(self.Clause)
        file.close()

class GetResult():
    # This class gets result after running smt program.

    # @param: smt file <code>model.smt</code>
    # @return: result sat/unsat
    # @return: statistics running data(runtime,memory)
    # @return: critical pair for sat situation
    # @return: unsat core for unsat situation(in progress)

    def __init__(self,filename,bound):
        self.bound = bound
        self.file = filename


    def Check(self):
        file = open(self.file, "a")
        #file.write("\n(check-sat)\n")
        file.write("(get-unsat-core)\n")
        #file.write("(get-info :all-statistics)\n")
        file.close


    def GetPath(self):
        file = open(self.file, "a")


        file.write("(get-value (")
        for i in range(0,self.bound + 1):
            file.write("(locFault " + str(i) + ")")
        file.write("))\n")


        file.write("(get-value (")
        for i in range(0, self.bound):
            file.write("(eventFault " + str(i) + ")")
        file.write("))\n")

        file.close

    def GetLength(self):
        file = open(self.file, "a")
        file.write("(get-value(lf))\n")
        file.close





























