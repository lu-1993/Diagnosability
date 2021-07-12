#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from transition import Transition


class Parser:
    def __init__(self):
        pass

    def parse(self, nameFile: str):
        automaton = []

        file = open(nameFile, "r")
        context = file.readlines()  # contest store all txt transitions and parameters

        initState = int(context[0].split(" ")[1])
        bound = int(context[0].split(" ")[3])
        delta = int(context[0].split(" ")[5])

        observable = context[0].split(" ")[6].split(
            "{")[1].split("}")[0].split(",")
        unobservable = context[0].split(" ")[7].split(
            "{")[1].split("}")[0].split(",")

        event_dict = defaultdict(int)

        for i in range(0, len(observable)):
            key = observable[i]
            value = i+3
            event_dict[key] = value
        for i in range(0, len(unobservable)):
            key = unobservable[i]
            value = 2
            event_dict[key] = value

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
            else:
                event = event_dict[event]
            # else:
             #   event = int(event.strip('o')) + 2

            guard = context[i].split(" ")[3].split(";")

            reset = context[i].split(" ")[4].split("\n")[0]
            resetList = []
            if reset != '0':
                for elt in reset.split(';'):
                    v = int(elt[1:])
                    resetList.append(v - 1)

            transition.append(sourceState)
            transition.append(finalState)
            transition.append(event)

            # print(guard)
            transition.append(guard)
            transition.append(resetList)

            automaton.append(Transition(
                sourceState, finalState, event, guard, resetList))

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

        for t in automaton:
            print(t)

        file.close()
        return initState, transitionList, bound, delta, len(clockList)
