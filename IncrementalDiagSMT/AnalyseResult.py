'''
/**
 * The goal is to analyse the result (sat or unsat) and acquire information
 * for the refinement in the next steps.
 * Before running this class, user should run smt format file at first,
 * get the result and stored it in file "result.txt"
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
**/
'''

from decimal import Decimal


class GetResult():

    def __init__(self,resultfile):
        self.file = open(resultfile,"r")

    # get the total time required for the verification
    def TotalTime(self):

        timelinelist = []
        text = self.file.readlines()

        for line in text:
            if "time" in line:
                timelinelist.append(line)

        timelist = []
        for i in timelinelist:
            time = Decimal(i.split("                    ")[1].split(")")[0])
            timelist.append(time)

        totaltime = "Time：" + str(sum(timelist))
        self.file.close()

        return totaltime

    # the function:
    # 1. get the faulty path <code>FaultyPath</code> of length lf in range(1,bound).
    # 2. get the normal path <code>NormalPath</code> of length ln in range(1,bound).
    # 3. check weather this two paths are critical pair.

    def SatOrUnsat(self):

        line = self.file.readline()
        parameter = line
        print(parameter)

        # get the length of faulty path
        FaultPathList = []
        NormalPathList = []
        FaultPathLengthBefore = 0
        FaultyPathLengthList = []

        final_length_ln = 0   #flag used to mark sat  0: unsat  other: sat

        while line:
            if line == "sat\n": # line: sat
                #if line is sat, this case should be stored.
                #structure: sat, echo(lf_b,current_ln_a),lf, faulty path(lf), ln, normal path(current_ln,a)
                line = self.file.readline()  # line: echo(lf_b,current_ln_a)
                CurrentNormalLength = len(line.split("a")) - 1


                line = self.file.readline()  #line : lf

                FaultPathLength = int(line.split(" ")[1].split("))")[0])


                if FaultPathLength != FaultPathLengthBefore:

                    FaultPathLengthBefore = FaultPathLength
                    FaultyPathLengthList.append(FaultPathLength)


                LocFaultSequence = []
                for i in range(0, FaultPathLength + 1):
                    line = self.file.readline()
                    LocFault = line.split(")")[1]
                    LocFaultSequence.append(LocFault)

                # get event sequence of faulty path
                EventFaultSequence = []
                #if "eventFault" in line:
                for i in range(0, FaultPathLength):
                    line = self.file.readline()

                    EventFault = line.split(")")[1]
                    EventFaultSequence.append(EventFault)



                #--------- get normal path of current_ln --------------#

                line = self.file.readline()  # line: ln


                ln = int(line.split(" ")[1].split(")")[0])


                LocList = []
                EventList = []

                # if return ln = current NL, result is sat, represent exist normal path which could construct a cretical pair with faulty path possiably.
                # the length of normal path from 1

                # else: result is unsat.
                # acquire the blocked event, in which one corresponding transition, and the process of constructing critical pair stops.

                if ln == CurrentNormalLength:

                    final_length_ln = CurrentNormalLength

                for i in range(0, CurrentNormalLength + 1):
                    line = self.file.readline()
                    loc = line.split(")")[1]
                    LocList.append(loc)

                for i in range(0, CurrentNormalLength):
                    line = self.file.readline()
                    event = line.split(")")[1]
                    EventList.append(event)



                # translate faulty path which are purely number format to original faulty path

                FaultPath = LocFaultSequence.copy()
                index = 1
                for i in range(0, len(EventFaultSequence)):
                    event = EventFaultSequence[i]
                    FaultPath.insert(index, event)
                    index = index + 2

                ObservableEventNum = len(parameter.split(' ')[4].split("={")[1].split("}")[0].split(","))

                UnobservableEventNum = len(parameter.split(' ')[5].split("={")[1].split("}")[0].split(","))

                # obsf used to stores observable sequence of faulty path
                obsf = []
                for i in range(1, len(FaultPath), 2):

                    if int(FaultPath[i]) <= ObservableEventNum:
                        TranslateEvent = "o" + str(FaultPath[i].split(' ')[1])
                        if len(obsf) == 0 or TranslateEvent != obsf[len(obsf)-1]:
                            obsf.append(TranslateEvent)

                    elif int(FaultPath[i]) > ObservableEventNum and int(
                            FaultPath[i]) <= ObservableEventNum + UnobservableEventNum:
                        TranslateEvent = "un" + str(int(FaultPath[i]) - int(ObservableEventNum))

                    else:
                        TranslateEvent = "f"

                    FaultPath[i] = TranslateEvent

                noteFaultyPath = "The faulty-path of length " + str(FaultPathLength) + " is:" + "\n"

                # FaultyPath is a faulty path sequence
                FaultyPath = parameter + noteFaultyPath + str(FaultPath) + "\n"

                FaultPathList.append(str(FaultPath))


                NormalPath = LocList.copy()


                index = 1
                for i in range(0, len(EventList)):
                    event = EventList[i]
                    NormalPath.insert(index, event)
                    index = index + 2

                ObservableEventNum = len(parameter.split(' ')[4].split("={")[1].split("}")[0].split(","))

                UnobservableEventNum = len(parameter.split(' ')[5].split("={")[1].split("}")[0].split(","))

                # obsn used to stores observable sequence of normal path
                obsn = []
                for i in range(1, len(NormalPath), 2):

                    if int(NormalPath[i]) <= ObservableEventNum:
                        TranslateEvent = "o" + str(NormalPath[i].split(' ')[1])
                        if len(obsn) == 0 or TranslateEvent != obsn[len(obsn) - 1]:
                            obsn.append(TranslateEvent)

                    elif int(NormalPath[i]) > ObservableEventNum and int(
                            NormalPath[i]) <= ObservableEventNum + UnobservableEventNum:
                        TranslateEvent = "un" + str(int(NormalPath[i]) - int(ObservableEventNum))

                    else:
                        TranslateEvent = "f"

                    NormalPath[i] = TranslateEvent

                NormalPathLength = len(LocList)


                #Normalpath = note + str(NormalPath) + "\n"
                NormalPathList.append(str(NormalPath))


            line = self.file.readline()

        FP = [] # store different faulty_path of different lf
        NP = [] # store corresponding normal_path


        if final_length_ln == 0:

            result = "UNSAT"
            critical_pair_number = len(FaultyPathLengthList)

            for i in range(1,critical_pair_number + 1 ):

                for j in range(0,len(FaultPathList)):
                    loc_num = len(FaultPathList[j].split(",")) - 1

                    if  loc_num/2 == FaultyPathLengthList[i-1]:

                        faulty_path = FaultPathList[j]
                        normal_path = NormalPathList[j]

                FP.append(faulty_path)
                NP.append(normal_path)


            print(result)
            for i in range(0,len(NP)):
                print(str(i+1) + ". possible critical pair:")
                print("the length of faulty path is: ", str(FaultyPathLengthList[i]))
                print(FP[i])
                print(NP[i])

                obsff = []  # stored all observables of faulty_path
                obsf = []  # stored observables eliminate same
                obsnn = []
                obsn = []
                for j in NP[i].split(","):
                    if 'o' in j:
                        obsnn.append(j)

                for i in FP[i].split(","):
                    if 'o' in i:
                        obsff.append(i)

                for i in obsnn:
                    if len(obsn) == 0:
                        obsn.append(i)
                    else:
                        if i != obsn[len(obsn)-1]:
                            obsn.append(i)

                for i in obsff:
                    if len(obsf) == 0:
                        obsf.append(i)
                    else:
                        if i != obsf[len(obsf)-1]:
                            obsf.append(i)

                flag = 1

                for i in range(0,len(obsn)):
                    if obsn[i] != obsf[i]:
                        block_event = obsf[len(obsn) - 1]
                        print("blocked in: ", block_event)
                        flag = 0
                        break


                while flag == 1:
                    block_event = obsf[len(obsn)]
                    print("blocked in: ", block_event)
                    break


        else:
            result = "SAT"

            for i in range(0,len(NormalPathList)):

                loc_num = len(NormalPathList[i].split(",")) - 1
                if loc_num/2 == final_length_ln :
                    faulty_path = FaultPathList[i]
                    normal_path = NormalPathList[i]

            FP.append(faulty_path)
            NP.append(normal_path)

            print(result)
            for i in range(0,len(NP)):
                print(str(i+1) + ". critical pair:")
                print("the length of faulty path is:", str(FaultyPathLengthList[i]))
                print(FP[i])
                print(NP[i])


            obsn = [] # all observable events
            obsnn = [] # eliminate same observable events
            for j in NP[i].split(","):
                if 'o' in j:
                    obsn.append(j)
            for i in obsn:
                if i not in obsnn:
                    obsnn.append(i)
            print("observables: ",obsnn)





