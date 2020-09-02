# RECAR
# IncrementDiagSMT
We show how to encode bounded diagnosability problem (critical pair as
a counterexample, please see the paper DiagnosabilityDES.pdf) for
finite automata in smt with the files available here, which are only
for a very simple example stored in model.txt. This simple system
contains six events, where three observable events are represented by
integers 1-3 and two unobservable normal events by 4-5 and one
unobservable faulty event by 6. There are ten transitions in this
system that one can find in the file model.txt beginning from line 2
(one transition per line). The file diagWithQuantifier.smt contains
the smt formula simplified from that is presented in the paper
DiagnosabilitySMTtimedAutomata.pdf, the latter is for timed automata.
The file diagNoQuantifier.smt is a quantifier-free version for the
same example. And result.txt contains a model satisfying the smt
formula, i.e., a critical pair which is a pair of trajectories of the
system where only one of them contains the fault while both of them
have the same observations.

An incremental version is also available in the IncrementDiagSMT
package, a python package that generates automatically smt formula in
an incremental way in terms of path length for this problem with
different parameters for a given system. To obtain the verification
result, it is enough to run the python file main.py that generates smt
formula, which is checked by calling z3 in an incremental way, whose
results are then analyzed before returning the final results.

for example in model.txt. 
The final result is:


If (7 o3 8) in model.txt, return:

Bound 5 K_value 2 observable={o1,o2,o3} unobservable={un1,un2} fault={f}

SAT

1. critical pair:

the length of faulty path is: 4

[' 1', 'o1', ' 2', 'o2', ' 3', 'f', ' 4', 'un1', ' 5', 'o3', ' 5']

[' 1', 'o1', ' 2', 'o2', ' 6', 'un2', ' 7', 'o3', ' 8']

observables:  [" 'o1'", " 'o2'", " 'o3'"]

Time：0.25


If (7 o2 8) in model.txt, return:

Bound 5 K_value 2 observable={o1,o2,o3} unobservable={un1,un2} fault={f}

UNSAT

1. critical pair possiablely :

the length of faulty path is:  4

[' 1', 'o1', ' 3', 'f', ' 4', 'un1', ' 5', 'o3', ' 5']

[' 1', 'o1', ' 2']

blocked in:   'o3'

2. critical pair possiablely :

the length of faulty path is:  5

[' 1', 'o1', ' 2', 'o2', ' 3', 'f', ' 4', 'un1', ' 5', 'o3', ' 5']

[' 1', 'o1', ' 2', 'o2', ' 6', 'un2', ' 7', 'o2', ' 8', 'o2', ' 8']

blocked in:   'o3'

Time：0.24

