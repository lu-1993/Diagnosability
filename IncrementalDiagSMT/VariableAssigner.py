'''
/**
 * The goal is to assign different integers to different states and events.
 *
 * A class <code>ParameterAssigner</code> to assign integers to k and bound value.
 * A class <code>EventAssigner</code> to assign integers to events
 * A class <code>transformModel</code> to translate transitions of original model to purely number file.
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
 *
 */
 '''
class ParameterAssigner():
    #This class to assign integers to bound, k.

    #:@param a string represent parameter.
    #:@return integer number represent k and bound.


    def __init__(self,parameter):

        self.parameterline = parameter

    def getBound(self):
        bound = int(self.parameterline.split(' ')[1])
        return bound

    def getKvalue(self):

        k = int(self.parameterline.split(' ')[3])
        return k


class EventAssigner():
    # This class to assign integers to events.

    # :@param a string represent parameter.
    # :@return list stores observable events.
    # :@return list stores unobservable events.
    # :@return list stores fault events.

    def __init__(self,parameter):

        self.parameterline = parameter

    def getObservableEventSet(self):
        # This function to extract observable events from the parameter line.

        # @:param a parameter line
        # @:return a list <code>list_obs</code> stores observable events

        s = self.parameterline.split(' ')[4]
        list_obs = s.split("={")[1].split("}")[0].split(",")
        return list_obs

    def getUnobservableEventSet(self):
        # This function to extract unobservable events from the parameter line.

        # @:param a parameter line
        # @:return a list <code>list_uno</code> stores unobservable events
        s = self.parameterline.split(' ')[5]
        list_uno = s.split("={")[1].split("}")[0].split(",")
        return list_uno

    def getFault(self):
        # This function to extract fault from the parameter line.

        # @:param a parameter line
        # @:return a list <code>fault</code> stores unobservable events
        s = self.parameterline.split(' ')[6].split('\n')[0]
        list_fau = s.split("={")[1].split("}")[0].split(",")
        return list_fau


    def getEventList(self):
        # This function to extract all events (containing fault) from the parameter line.

        # @:param a parameter line
        # @:return a list <code>fault</code> stores normal events
        s1 = self.parameterline.split(' ')[4]
        list_obs = s1.split("={")[1].split("}")[0].split(",")

        s2 = self.parameterline.split(' ')[5]
        list_uno = s2.split("={")[1].split("}")[0].split(",")

        s3 = self.parameterline.split(' ')[6].split('\n')[0]
        list_fau = s3.split("={")[1].split("}")[0].split(",")


        # if unobservable is null, then eventlist is observable+fault. it is to ensure that eventset has no null list,
        # which result the index of fault is wrong.
        # In our algorithm, we have at least one observable event, and at least one fault.
        # so only need consider the case where there is no unobservable events.
        if list_uno[0] == '':

            list_event = list_obs + list_fau
        else:


            list_event = list_obs + list_uno + list_fau

        return list_event

    def NormalEventSet(self):
        # This function to extract normal events(no fault) from the parameter line.

        # @:param a parameter line
        # @:return a list <code>fault</code> stores normal events
        s1 = self.parameterline.split(' ')[4]
        list_obs = s1.split("={")[1].split("}")[0].split(",")

        s2 = self.parameterline.split(' ')[5]
        list_uno = s2.split("={")[1].split("}")[0].split(",")

        s3 = self.parameterline.split(' ')[6].split('\n')[0]
        list_fau = s3.split("={")[1].split("}")[0].split(",")


        # if unobservable is null, then eventlist is observable+fault. It eusures eventset has no null list,
        # which result the index of fault is wrong.
        # In our algorithm, we assume there is at least one observable event, and at least one fault.
        # so only need consider the case where there is no unobservable events.

        if list_uno[0] == '':

            list_normalEvent = list_obs
        else:


            list_normalEvent = list_obs + list_uno

        return list_normalEvent



    def eventIndex(event,eventlist):
        # This function assign integers to events
        # In our algorithm, assign integers to observable events begins from 1,
        # then assign integers to unobservable events
        # finally assign fault in order.

        # :@param a single event, a eventlist stores all events
        # :@return integer represent event

        for i in range(0,len(list)):
            if event == list[i]:
                return str(i+1)
            return "null"


class transformModel():
    # This class translates original transitions after assigning integers to events and states.
    # The results are written in an external smt file <code>modelsmt</code>

    # :@param a <code>modelstr</code> stores original transitions of model.
    # :@param a <code>listevent</code> stores all events
    # :@return a external smt file <code>modelsmt</code> stores all transitions after translation.

    def __init__(self,modelstr,modelsmt,listevent):
        file = open(modelsmt,"w")
        listTrans = modelstr.split('\n')
        for i in range(0,len(listTrans)-1):

            file.write(listTrans[i].split(' ')[0] + " " + listTrans[i].split(' ')[2])
            event = listTrans[i].split(' ')[1]

            # if observable events and unobservable events are un-complete, we write event as 0
            eventStr = " " + str(0) + "\n"

            for j in range(0,len(listevent)):


                if event == listevent[j]:

                    # if observable event and unobservable event are complete

                    eventStr = " " + str(j+1) + "\n"


            file.write(eventStr)


        file.close()
