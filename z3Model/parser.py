#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Parser:
    def __init__(self):
        pass


        def parse(self, nameFile : str):

        file = open(nameFile, "r")
        context = file.readlines()

        initState = context[0].split(" ")[1]
        bound = context[0].split(" ")[3]
        k = context[0].split(" ")[5]

        transitionList = []
        for i in range(1, len(context)):
            transition = []


            sourceState = int(context[i].split(" ")[0]) - int(initState)
            event = context[i].split(" ")[1]
            finalState = int(context[i].split(" ")[2].split("\n")[0]) - int(initState)

            if event == "f":
                event = 0
            elif "u" in event:
                event = 1
            else:
                event = int(event.strip('o')) + 1

            transition.append(sourceState)
            transition.append(finalState)
            transition.append(event)


            transitionList.append(transition)


        file.close()

        return initState,transitionList,bound,k

