#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Parser:
    def __init__(self,nameFile : str):
        self.file = nameFile


    def parse(self):

        file = open(self.file, "r")
        context = file.readlines()

        initState = context[0].split(" ")[1]

        transitionList = []
        for i in range(1, len(context)):

            sourceState = int(context[i].split(" ")[0]) - int(initState)
            event = context[i].split(" ")[1]
            finalState = int(context[i].split(" ")[2].split("\n")[0]) - int(initState)

            if event == "f":
                event = 0
            elif "u" in event:
                event = 1
            else:
                event = int(event.strip('o')) + 1

            transition = (sourceState, finalState, event)

            transitionList.append(transition)

        model = initState + " " + str(transitionList)
        
        file.close()

        return model



        #return 0, [(0,1,2),(1,2,1),(1,2,0),(2,3,1),(2,4,0),(3,3,3),(4,4,4)]

