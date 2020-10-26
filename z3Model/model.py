#!/usr/bin/python3
# -*- coding: utf-8 -*-

from z3 import *
from parser import Parser

# Here are some suppositions:
# The NOP operation is represented by no observable that repeat.

# the solver instance.
s = Solver()

BOUND = 10
K = 4

# the automata.
assert(len(sys.argv) == 2)
p = Parser()
initState, transitionList = p.parse(sys.argv[1])
transitionList.sort(key=lambda t: t[2])

# get information about the automata.
limitFaulty = 0
limitNoObser = 0
observableId = []

nextTransition = [[] for i in range(len(transitionList))]
for i in range(len(transitionList)):
    if transitionList[i][2] == 0:
        limitFaulty = i + 1
    elif transitionList[i][2] == 1:
        limitNoObser = i + 1
    else:
        if transitionList[i][2] not in observableId:
            observableId.append(transitionList[i][2])

    for j in range(len(transitionList)):
        if (transitionList[i][1] == transitionList[j][0]):
            nextTransition[i].append(j)

# get the transition that are valid with the initial init state.
possibleInitialTransition = []
for i in range(len(transitionList)):
    if transitionList[i][0] == initState:
        possibleInitialTransition.append(i)

print("Information ...")
print("automata:")
for i in range(len(transitionList)):
    print(i, ":", transitionList[i])

print("next transition:")
for i in range(len(nextTransition)):
    print(i, ':', nextTransition[i])

print("possible init transition: ", possibleInitialTransition)
print("limitFaulty:", limitFaulty)
print("limitNoObser:", limitNoObser)

# we create the variables that will be used to represent the path.
faultyPath = [ Int("fp_" + str(i+1)) for i in range(BOUND) ]
normalPath = [ Int("np_" + str(i+1)) for i in range(BOUND) ]
idTransitionFaultyPath = [ Int("idt_fp_" + str(i+1)) for i in range(BOUND) ]
idTransitionNormalPath = [ Int("idt_np_" + str(i+1)) for i in range(BOUND) ]
nopFaultyPath = [ Bool("nop_fp_" + str(i+1)) for i in range(BOUND) ]
nopNormalPath = [ Bool("nop_np_" + str(i+1)) for i in range(BOUND) ]

s.add([ faultyPath[i] < len(transitionList) for i in range(BOUND) ])
s.add([ normalPath[i] < len(transitionList) for i in range(BOUND) ])
s.add([ idTransitionFaultyPath[i] < len(observableId) + 2 for i in range(BOUND) ])
s.add([ idTransitionNormalPath[i] < len(observableId) + 2 for i in range(BOUND) ])

# constraints on the first transition.
s.add(Or([faultyPath[0] == v for v in possibleInitialTransition]))
s.add(Or([normalPath[0] == v for v in possibleInitialTransition]))

# we have a fault soon enough.
s.add(Or([faultyPath[i] < limitFaulty for i in range(len(transitionList) - K)]))

# verify that the transition are correct.
for i in range(1, len(faultyPath)):
    for j in range(len(transitionList)):
        if transitionList[j][2] == 2:
            s.add(Implies(faultyPath[i-1] == j, Or([faultyPath[i] == n for n in nextTransition[j]])))
            s.add(Implies(normalPath[i-1] == j, Or([normalPath[i] == n for n in nextTransition[j]])))
        else:
            # we can always repeat no observable transition to simulate NOP.
            s.add(Implies(faultyPath[i-1] == j, Or(faultyPath[i] == j, Or([faultyPath[i] == n for n in nextTransition[j]]))))
            s.add(Implies(normalPath[i-1] == j, Or(normalPath[i] == j, Or([normalPath[i] == n for n in nextTransition[j]]))))

# no fault in the normal path.
s.add(And([x >= limitFaulty for x in normalPath]))

# two paths have to agree on the observables.
# first we collect the id:
for i in range(len(faultyPath)):
    for j in range(limitNoObser):
        s.add(Implies(faultyPath[i] == j, idTransitionFaultyPath[i] == 0))
        s.add(Implies(normalPath[i] == j, idTransitionNormalPath[i] == 0))

    for j in range(limitNoObser, len(transitionList)):
        s.add(Implies(faultyPath[i] == j, idTransitionFaultyPath[i] == transitionList[j][2]))
        s.add(Implies(normalPath[i] == j, idTransitionNormalPath[i] == transitionList[j][2]))

# second we have identical id
for i in range(len(idTransitionFaultyPath)):
    s.add(idTransitionFaultyPath[i] == idTransitionNormalPath[i])

# check the NOP status.
s.add(nopFaultyPath[0] == False)
s.add(nopNormalPath[0] == False)

for i in range(1, len(faultyPath)):
    s.add(nopFaultyPath[i] == (And(faultyPath[i] < limitNoObser, faultyPath[i-1] == faultyPath[i])))
    s.add(nopNormalPath[i] == (And(normalPath[i] < limitNoObser, normalPath[i-1] == normalPath[i])))

# we want to progress
for i in range(1, len(faultyPath)):
    s.add(Or(Not(nopFaultyPath[i]), Not(nopNormalPath[i])))

# breaking symmetries in the nop schema
for i in range(1,len(faultyPath)):
    s.add(Implies(nopFaultyPath[i-1], Or(nopFaultyPath[i], idTransitionFaultyPath[i] != 0)))
    s.add(Implies(nopNormalPath[i-1], Or(nopNormalPath[i], idTransitionNormalPath[i] != 0)))

print(s)

res = s.check()
if res == sat:
    m = s.model()

    # print the paths
    print("Faulty path:")
    for i in range(len(faultyPath)):
        v = int(m.evaluate(faultyPath[i]).as_long())
        id = int(m.evaluate(idTransitionFaultyPath[i]).as_long())
        nop = m.evaluate(nopFaultyPath[i])
        assert(id == 0 or transitionList[v][2] == id)
        print(transitionList[v],id,nop, end=" ")
    print()

    print("Normal path:")
    for i in range(len(normalPath)):
        v = int(m.evaluate(normalPath[i]).as_long())
        id = int(m.evaluate(idTransitionNormalPath[i]).as_long())
        nop = m.evaluate(nopNormalPath[i])
        assert(id == 0 or transitionList[v][2] == id)
        print(transitionList[v],id,nop,end=" ")
    print()
else:
    print("it is unsat")
