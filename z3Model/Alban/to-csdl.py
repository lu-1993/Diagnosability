import sys
import re
from typing import Tuple, List, Set

def print_usage(): 
    print("Usage: python to-csdl.py input_file output_prefix")
    print("The output files will be: ")
    print("  $output_prefix.dmdl")
    print("  $output_prefix.codl")
    print("  $output_prefix.csdl")

def read_file(filename) -> Tuple[Set[str],str,Set[str],Set[str],Set[str],List[Tuple[str,str,str]]]: 
    # returns: list of states, initial state, list of unobs, list of obs, list of faults, list of transitions
    states = set()
    init = ''
    unobs = set()
    obs = set()
    faults = set()
    transes = []

    import re

    first_line_pattern = 'Initial_state\s+([^\s]+)\s+Bound\s+([^\s]+)\s+observable={([^\}]+)}\s+unobservable={([^\}]+)}\s+fault={([^\}]+)}\s+'
    trans_pattern = '\s*([^\s]+)\s+([^\s]+)\s+([^\s]+)\s*'

    with open(filename) as file: 
        first_line = file.readline()
        first = re.findall(first_line_pattern, first_line)
        if len(first) != 1:
            print('Problem reading line 1: {}'.format(first_line))
            exit(2)
        first = first[0]
        init = first[0]
        obs = set(first[2].split(','))
        unobs = set(first[3].split(','))
        faults = set(first[4].split(','))

        for line in file:
            trans = re.findall(trans_pattern, line)
            if len(trans) == 1:
                tr = trans[0][0], trans[0][1], trans[0][2]
                transes.append(tr)
                states.add(tr[0])
                states.add(tr[2])

    return states, init, unobs, obs, faults, transes

def print_dmdl(auto: Tuple[Set[str],str,Set[str],Set[str],Set[str],List[Tuple[str,str,str]]], 
        filename: str):
    states = auto[0]
    init = auto[1]
    unobses = auto[2]
    obses = auto[3]
    fes = auto[4]
    transes = auto[5]
    with open(filename, 'w') as out:
        out.write('Component (output unobs, output obs, output f)\n')
        out.write('{\n')

        out.write('  variables:\n')
        # gotta make sure the initial state is first!
        out.write('    state in {s' + init)
        for state in states:
            if state != init:
                out.write(',s' + state)
        out.write('}\n')
        # adding an s to the name of the states because I am not sure the parser can take numbers

        out.write('\n')
        out.write('  events:\n')
        out.write('    spontaneous: ')
        for i in range(len(transes)): # one event per transition
            if i != 0:
                out.write(',')
            out.write('spon{}'.format(i))
        out.write(';\n')
        out.write('    unobs: ' + ','.join(unobses) + ';\n')
        out.write('    obs: ' + ','.join(obses) + ';\n')
        out.write('    f: ' + ','.join(fes) + ';\n')

        i = 0
        for origin, event, target in transes:
            port = ''
            if event in unobses:
                port = 'unobs'
            elif event in obses:
                port = 'obs'
            elif event in fes:
                port = 'f'
            else: 
                print('Unknown event {}'.format(event))
                exit(3)
            out.write('\n')
            out.write('  require (state=s{})\n'.format(origin))
            out.write('    when spon{}\n'.format(i))
            out.write('    output {}.{}\n'.format(port, event))
            out.write('    effect (state=s{})\n'.format(target))
            i += 1

        out.write('}\n')

def print_codl(filename):
    with open(filename, 'w') as out:
        out.write('Component c;\n')
        out.write('Initial configuration: c;\n')
        out.write('observe(c.obs);\n')
    pass

def print_csdl(filename, dmdlfile, codlfile):
    with open(filename, 'w') as out:
        out.write('System {\n')
        out.write('  library:\n')
        out.write('    insert \'{}\'\n'.format(dmdlfile))
        out.write('  domain:\n')
        out.write('    insert \'{}\'\n'.format(codlfile))
        out.write('  reconfigurations:\n')
        out.write('}\n')
    pass

def print_faults(filename, faultevents):
    with open(filename, 'w') as out:
        for fault in faultevents:
            out.write('c f {}\n'.format(fault))
    pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        exit(1)

    auto = read_file(sys.argv[1])

    suffix = re.findall('([^/]+)$', sys.argv[2])
    if len(suffix) != 1:
        print('Issue with filename {}'.format(sys.argv[2]))
        exit(4)
    suffix = suffix[0]

    print_dmdl(auto, sys.argv[2] + '.dmdl')
    print_codl(sys.argv[2] + '.codl')
    print_csdl(sys.argv[2] + '.csdl', suffix + '.dmdl', suffix + '.codl')
    print_faults(sys.argv[2] + '.fault', auto[4])


    print("KTHXBAY")
