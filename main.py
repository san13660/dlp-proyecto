from graphviz import Digraph
from tree import Node, initial_node, separate_children
from automaton import State, Transition, AF
from thompson import process
from subset import create_afd
from direct import find_tree_values, create_direct_afd
from simulation import simulate_afd, simulate_afn

import time

def check_for_errors(rules):
    open_p = rules.count('(')
    close_p = rules.count(')')

    if(open_p > close_p):
        raise Exception("Parentesis invalidos, falta -> )")
    
    if(close_p > open_p):
        raise Exception("Parentesis invalidos, falta -> (")

    if('|*' in rules):
        raise Exception("Operadores invalidos -> |*")
    
    if('|?' in rules):
        raise Exception("Operadores invalidos -> |?")

    if('|+' in rules):
        raise Exception("Operadores invalidos -> |+")

    if('|)' in rules):
        raise Exception("Operador invalido -> |)")

    if('(|' in rules):
        raise Exception("Operador invalido -> (|")

def fix_errors(rules):
    rules_fixed = rules
    if('()' in rules):
        rules_fixed = rules_fixed.replace('()','')

    return rules_fixed

flag = True
while(flag):
    rules = input('\nIngrese la expresion regular: ')

    try:
        check_for_errors(rules)
        rules = fix_errors(rules)

        print('\n---Creando arbol---\n')

        tree = Node.initialize_tree(rules)
        alphabet = separate_children(tree)
        flag=False
    except Exception as e:
        print('\n** ERROR: {} **'.format(e))


tree.graph_tree('Arbol_AFN_Thompson', 'Arbol (AFN Thompson) - {}'.format(rules))

#---------------------------------------------------------

print('\n---Creando AFN por metodo de Thompson---\n')

afn = process(tree)

afn.assign_state_numbers()
afn.graph_fsm('AFN_Thompson', 'AFN (Thompson) - {}'.format(rules))

#---------------------------------------------------------------

print('\n---Creando AFD por subconjuntos---\n')

afd = create_afd(afn, alphabet)
#afd.assign_state_numbers()
afd.graph_fsm('AFD_Subconjuntos', 'AFD (Subconjuntos) - {}'.format(rules))

#--------------------------------------------------------------

print('\n---Creando AFD por metodo directo---\n')

new_tree, symbol_ids = find_tree_values(tree)
new_tree.graph_tree('Arbol_Directo', 'Arbol (AFD Directo) - {}'.format(rules),show_pos=True)

afd_direct = create_direct_afd(new_tree,symbol_ids,alphabet)
#afd_direct.assign_state_numbers()
afd_direct.graph_fsm('AFD_Directo', 'AFD (Directo) - {}'.format(rules))

#-----------------------------------------------------------

while(True):
    string = input('\nIngrese cadena a evaluar: ')
    print('\n-------------SIMULACION-----------------')
    
    t0 = time.perf_counter()
    result_afn = simulate_afn(afn, string)
    t1 = time.perf_counter()
    print('AFN: {}'.format(result_afn))
    print("Time elapsed: {}s".format(t1 - t0))

    t0 = time.perf_counter()
    result_afd_subset = simulate_afd(afd, string)
    t1 = time.perf_counter()
    print('\nAFD (Subconjuntos): {}'.format(result_afd_subset))
    print("Time elapsed: {}s".format(t1 - t0))

    t0 = time.perf_counter()
    result_afd_direct = simulate_afd(afd_direct, string)
    t1 = time.perf_counter()
    print('\nAFD (Directo): {}'.format(result_afd_direct))
    print("Time elapsed: {}s".format(t1 - t0))

