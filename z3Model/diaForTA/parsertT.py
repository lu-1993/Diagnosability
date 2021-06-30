#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Parser:
    def __init__(self):
        pass

    def parse(self, nameFile: str):

        file = open(nameFile, "r")
        context = file.readlines()  # contest store all txt transitions and parameters

        initState = int(context[0].split(" ")[1])
        bound = int(context[0].split(" ")[3])
        delta = int(context[0].split(" ")[5])

        clockString = context[0].split(" ")[9]
        clockList = clockString.split("{")[1].split("}")[0].split(",")

        transitionNum = 0
        for i in range(1, len(context)):
            transitionNum += 1
            if context[i] == '\n':
                break

        transitionList = []
        for i in range(1, transitionNum):

            transition = []

            sourceState = int(context[i].split(
                " ")[0].split(',')[0]) - int(initState)
            finalState = int(context[i].split(
                " ")[2].split(',')[0]) - int(initState)
            event = context[i].split(" ")[1]

            if event == "f":
                event = 1
            elif "u" in event:
                event = 2
            else:
                event = int(event.strip('o')) + 2

            guard = context[i].split(" ")[3].split(";")

            reset = context[i].split(" ")[4].split("\n")[0]

            transition.append(sourceState)
            transition.append(finalState)
            transition.append(event)
            transition.append(guard)
            transition.append(reset)

            transitionList.append(transition)

        maxstate = 0
        for i in transitionList:
            currentState = int(i[0])
            if currentState > maxstate:
                maxstate = currentState
            currentState = int(i[1])
            if currentState > maxstate:
                maxstate = currentState

        invariantsList = [1 for i in range(0, maxstate+1)]

        for i in range(transitionNum+2, len(context)):
            state = int(context[i].split(' ')[0])
            inv = context[i].split(' ')[1].split("\n")[0]
            invariantsList[state] = inv

        for transition in transitionList:
            state = int(transition[0])
            transition.insert(1, invariantsList[state])
            state = int(transition[2])
            transition.insert(3, invariantsList[state])

        file.close()
        return initState, transitionList, bound, delta, len(clockList)
