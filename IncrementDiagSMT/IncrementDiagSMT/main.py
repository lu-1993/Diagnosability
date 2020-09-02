'''
/**
* This python package generates automatically smt formula to check
* bounded diagnosability problem (critical pair as a counterexample,
* please see the paper DiagnosabilityDES.pdf) for finite automata,
* this problem with different parameters for any given system (finite automata or timed automata).

* This version adopts incremental way to verify diagnosablility.

* To change models, user could edit <file>model.txt</file>

* @author Lulu HE
* @Email helulu@lri.fr


**/
'''

import os
import InputSteam
import VariableAssigner
import VariableSemantic
import PathConstraint
import ClauseSteam
import AnalyseResult
import checksat
import distance


'''
/**
* The following part implements:
* 1. Read the orginal model from model.txt file. 
* The first line of model.txt is parameters:  <k, bound, Events Set>,
* and the next lines are transitions of the original system, one transition per line.

* 2. Assign events and states with different integers.
* After assigning, transform transitions of original model to purely numbers file 
* and stored in <file>modelsmt.txt</file>.
* This purely number file could be read by SMT slover Z3 directly.

@:param original model stored in <code>model.txt</code>
@:return the value of k.
@:return the value of bound.
@:return different event sets.
@:return <file>modelsmt.txt</file> is a purely number file stores transformed transitions of original model.
**/
'''


inputData = InputSteam.InputGet("model.txt")
parameter = inputData.parameter
model = inputData.model

# read parameters of system (finite automata) including k; bound; observable event set; unboservable event set; fault set.
variable = VariableAssigner.ParameterAssigner(parameter)
bound =  variable.getBound()
k = variable.getKvalue()
event = VariableAssigner.EventAssigner(parameter)
obseverableEventSet = event.getObservableEventSet()
unobservableEventSet = event.getUnobservableEventSet()
NormalEventSet = event.NormalEventSet()
fault = event.getFault()

#evnetSet includes all events
eventSet = event.getEventList()


# Assign integer number to events and states, transform original model (<code>model</code>)
# to a <file>modelsmt</file> composed purely of numbers.
modelsmt = VariableAssigner.transformModel(model,"modelsmt.txt",eventSet)

'''
/**
* The following part implements:
* Generate smt formula representing a critical pair that meets different conditions
* based on the parameters (k and bound) and transitions data
* in purely number file <code>modelsmt.txt</code>

* In this algorithm, there are two paths, a normal path and a faulty path.
* To distinguish the value of variables between the two paths,
* the variables equipped with a "Fault" are associated to the faulty trajectory,
* the variables without a "Fault" are associated to the normal trajectory.

@:param k; bound; purely number transitions stored in <code>modelsmt.txt</code> 
@:return Smt format statements represented by different 'String'
**/
'''

# Initialize the model
# declare use unsat core
# declare datatype to store transitions of model.

InitModel = InputSteam.InitModel()
InitSetUnsatStr = InitModel.InitSet()
DeclareTranstionsStr =  InitModel.DecalreTransitionsDatetpyes()

#read <file>modelsmt.txt</file>, transform model represented by purely number txt to smt format.
transform = InputSteam.TransformTransitions("modelsmt.txt")
TransitionsStr = transform.TransformTransition()



# declare transitions of normal path.
# 1: random value (this parameter is useless for InitFlag)
DealareNormalTransition = PathConstraint.NormalPathConstraint(1,k,bound).InitFlag()

# declare transitions of faulty path.
# 1: random value
DealareFaultyTransition = PathConstraint.FaultyPathConstraint(1,k,bound).InitFlag()

# function to verify whether a given event (integer) is an observable event;
# if observable, return true, otherwise, return false.
eventSemantic = VariableSemantic.observableEvent(obseverableEventSet)
eventSemanticStr = eventSemantic.observableEventSemantic()

# function to verify whether a given transitions associated with a fault,
# if yes. return true, otherwise, return false;
existFSemantic = VariableSemantic.existFault(NormalEventSet)
existFSemanticStr = existFSemantic.existFaultSemantic()

# function to verify whether a given transitions associated without a fault,
# if yes. return true, otherwise, return false;
notFSemantic = VariableSemantic.notFault(NormalEventSet)
notFSemanticStr = notFSemantic.notFaultSnmantic()

# initialization the path.
# define event <code>InitEventStr</code>; define state <code>InitLocStr</code>.
Init = PathConstraint.Init()
InitEventStr = Init.InitEvent()
InitLocStr = Init.InitState()

# some functions to computer k-value on the specific transition
# (k represents the number of steps after the fault) <code>ComputerKStr</code>
ComputerK = PathConstraint.ComputerK(NormalEventSet)
NoteComputerK = ComputerK.note()
IFautlStr = ComputerK.iFault()
IsFault = ComputerK.IsFault()
KValue = ComputerK.KValue()
Midk = ComputerK.ComputerIsFault()
CompK = ComputerK.ComputerK()
ComputerKStr = NoteComputerK + IFautlStr + IsFault + KValue + Midk + CompK

# declare length of normal path <code>LengthNormalPathStr</code>
# and faulty path <code>LengthFaultyPathStr</code>.
LengthPath = PathConstraint.LengthPath()
LengthNoteStr = LengthPath.note()
LengthNormalPathStr = LengthPath.NormalPathLength()
LengthFaultyPathStr = LengthPath.FaultyPathLength()
InitLengthStr = LengthNoteStr + LengthNormalPathStr + LengthFaultyPathStr

#declare two arrays obsn: array <code>NormalArrayStr</code> to store all observable events on the normal path.
# obsf: array <code>FaultyArrayStr</code> to store all observable events on the faulty path;
Array = PathConstraint.Array()
ArrayNoteStr = Array.note()
NormalArrayStr = Array.NormalArray()
FaultyArrayStr = Array.FaultyArray()

'''
/**
* The following part implements:
* 1. Generate faulty path with length bound.
* 2. Generate normal path with length bound. 


@:param k; bound;  <file>modelsmt.txt</file> 
@:return BoundNormalPath is a list storing bounded number transitions of a normal path.
@:return BoundFaultyPath is a list storing bounded number transitions of a faulty path.

**/
'''


BoundNormalPath = []
for i in range(0, bound):

    # create the i_th transition of the normal path.
    CreateNormalPath = PathConstraint.CreatePath("modelsmt.txt", i)
    NormalConstraint = PathConstraint.NormalPathConstraint(i, k, bound)
    NormalPathTransitionsStr = CreateNormalPath.CreateNormalPath()

    # store observables events of the i_th transition of normal path to 'obsn' array
    GetObservableEventStr = NormalConstraint.ObservableEventArray()


    #ensure not fault in i_th transition
    NotFaultOccur = NormalConstraint.NotFaultOccur()

    # check weather the observable events sequence of normal path as same as fautly path.
    ObservableEquivlence = NormalConstraint.Equivalent()

    # Verify this i_th transition
    VerifyTransition = NormalConstraint.TransitionVeirfy()

    # add all constraints of i_th transition are satisfied.
    NormalPath = []
    NormalPath.append(NormalPathTransitionsStr)
    NormalPath.append(GetObservableEventStr)
    NormalPath.append(NotFaultOccur)
    NormalPath.append(ObservableEquivlence)
    NormalPath.append(VerifyTransition)



    # conjunction all conditions of the i_th transition .
    NormalTransitionWithConstranint = ClauseSteam.LinkClause(NormalPath).Conjunction()

    # named i_th transition
    NamedNormalTransiton = ClauseSteam.NamedClause(i, NormalTransitionWithConstranint).NamedNormalTransition()

    # assert i_th transition
    AssertClause = ClauseSteam.Assert(NamedNormalTransiton).Assert()

    # BoundNormalPath stores all transitions of the normal path.
    NormalTransition = AssertClause
    BoundNormalPath.append(NormalTransition)

# transform list to string
BoundNormalPathStr = ""
for transition in BoundNormalPath:
    BoundNormalPathStr = BoundNormalPathStr + transition


BoundFaultyPath = []
for i in range(0,bound):

    # create the i_th transition of the normal path.
    CreateFaultyPath = PathConstraint.CreatePath("modelsmt.txt",i)
    FaultyConstraint = PathConstraint.FaultyPathConstraint(i, k, bound)
    FaultyPathTransitionsStr = CreateFaultyPath.CreateFaultyPath()

    # computer k value of this i_th transition
    Kcomputer = FaultyConstraint.ComputerK()

    # store observables events of the i_th transition of normal path to 'obsf' array
    GetObservableEventStr = FaultyConstraint.ObservableEventArray()

    # based k value get the length of faulty path.
    VerifyK = FaultyConstraint.VerifyK()

    # add all constraints of i_th transition  are satisfied.
    FaultyPath = []
    FaultyPath.append(FaultyPathTransitionsStr)
    FaultyPath.append(Kcomputer)
    FaultyPath.append(GetObservableEventStr)
    #FaultyPath.append(VerifyK)

    # conjunction all conditions of the i_th transition .
    FaultyTransitionWithConstranint = ClauseSteam.LinkClause(FaultyPath).Conjunction()

    # named i_th transition
    NamedFaultyTransiton = ClauseSteam.NamedClause(i, FaultyTransitionWithConstranint).NamedFaultyTransition()

    # assert i_th transition
    AssertClause = ClauseSteam.Assert(NamedFaultyTransiton).Assert()

    # BoundFaultyPath stores all transitions of the faulty path.
    FaultyTransition = AssertClause
    BoundFaultyPath.append(FaultyTransition)

# transform list to string
BoundFaultyPathStr = ""
for transition in BoundFaultyPath:
    BoundFaultyPathStr = BoundFaultyPathStr + transition

'''
/**
* The following part implements:
# check weather a faulty path and a normal path of length in range(1,bound+1).

# In our algorithm, the existence of a normal path of length in range(1, bound+1),
# with a faulty path as a critical pair, witnesses non diagnosability of the given system(finite automata)
# otherwise, the system is diagnosable.

@:param k; bound;  
@:return check-sat statements


**/
'''

min_bound = int(distance.min_f_distance) + k # the minimize length of faulty path which satisfy k and f
check = []

for i in range(min_bound-1,bound):
    #  i is the length of faulty path
    for j in range(1,bound+1):
        # j is the length of normal path
        check.append(checksat.CheckSat(k,j,i).check())


# transform list to string
checkstr = ""
for clause in check:
    checkstr = checkstr + clause

'''
/**
* The following part implements:
# 1. Create smt file <file>model_incremental.smt</file>, write all smt formulas in an incremental way.
# 2. run <file>model_incremental.smt</file>, stores result to file <file>result.txt</file>

@:param <file>model_incremental.smt</file>;  
@:return file <file>result.txt</file>

**/
'''
#create smt file<code>model.smt</code>, write all smt formulas,
#clare .smt format file

file = "model_incremental.smt"
open(file,"w").truncate()

ClauseSteam.GenerateSMT(file,InitSetUnsatStr).write()
ClauseSteam.GenerateSMT(file,DeclareTranstionsStr).write()
ClauseSteam.GenerateSMT(file,TransitionsStr).write()
ClauseSteam.GenerateSMT(file,DealareNormalTransition).write()
ClauseSteam.GenerateSMT(file,DealareFaultyTransition).write()
ClauseSteam.GenerateSMT(file,eventSemanticStr).write()
ClauseSteam.GenerateSMT(file,InitEventStr).write()
ClauseSteam.GenerateSMT(file,InitLocStr).write()
ClauseSteam.GenerateSMT(file,InitLengthStr).write()
ClauseSteam.GenerateSMT(file,ComputerKStr).write()
ClauseSteam.GenerateSMT(file,existFSemanticStr).write()
ClauseSteam.GenerateSMT(file,notFSemanticStr).write()
ClauseSteam.GenerateSMT(file,FaultyArrayStr).write()
ClauseSteam.GenerateSMT(file,NormalArrayStr).write()
#ClauseSteam.GenerateSMT(file,assertK).write()


ClauseSteam.GenerateSMT(file,BoundNormalPathStr).write()
ClauseSteam.GenerateSMT(file,BoundFaultyPathStr).write()
ClauseSteam.GenerateSMT(file,checkstr).write()




#run smt file, get result and stores it to the <file>result.txt</file>
file = open("result.txt","w")
file.write(parameter)
file.close()
os.system("z3 -smt2 model_incremental.smt >> result.txt")

'''
/**
* The following part implements:
# Analyse result returned. get time, critical pair, blocked event.

@:param <file>result</file>;  
@:return result

**/
'''

totaltime = AnalyseResult.GetResult("result.txt").TotalTime()
result = AnalyseResult.GetResult("result.txt").SatOrUnsat()

print(totaltime)


#---------------- run algorithm ---------------------#
























