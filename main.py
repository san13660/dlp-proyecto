from graphviz import Digraph
from tree import Node, initial_node, separate_children
from automaton import State, Transition, AF
from thompson import process
from subset import create_afd
from direct import find_tree_values, create_direct_afd
from simulation import simulate_afd, simulate_afn

import time

rules = input('Ingrese la expresion regular: ')

print('\n---Creando arbol---\n')

tree = Node.initialize_tree(rules)
alphabet = separate_children(tree)

tree.graph_tree('Arbol_AFN_Thompson', 'Arbol (AFN Thompson) - {}'.format(rules))

#---------------------------------------------------------

print('\n---Creando AFN por metodo de Thompson---\n')

afn = process(tree)

afn.assign_state_numbers()
afn.graph_fsm('AFN_Thompson', 'AFN (Thompson) - {}'.format(rules))

#---------------------------------------------------------------

print('\n---Creando AFD por subconjuntos---\n')

afd = create_afd(afn, alphabet)
afd.assign_state_numbers()
afd.graph_fsm('AFD_Subconjuntos', 'AFD (Subconjuntos) - {}'.format(rules))

#--------------------------------------------------------------

print('\n---Creando AFD por metodo directo---\n')

new_tree, symbol_ids = find_tree_values(tree)
new_tree.graph_tree('Arbol_Directo', 'Arbol (AFD Directo) - {}'.format(rules),show_pos=True)

afd_direct = create_direct_afd(new_tree,symbol_ids,alphabet)
afd_direct.assign_state_numbers()
afd_direct.graph_fsm('AFD_Directo', 'AFD (Directo) - {}'.format(rules))

#-----------------------------------------------------------

while(True):
    string = input('\nIngrese cadena a evaluar: ')
    print('\n-------------SIMULACION-----------------')
    
    t0 = time.perf_counter()
    print('AFN: {}'.format(simulate_afn(afn, string)))
    t1 = time.perf_counter()
    print("Time elapsed: {}s".format(t1 - t0))

    t0 = time.perf_counter()
    print('\nAFD (Subconjuntos): {}'.format(simulate_afd(afd, string)))
    t1 = time.perf_counter()
    print("Time elapsed: {}s".format(t1 - t0))

    t0 = time.perf_counter()
    print('\nAFD (Directo): {}'.format(simulate_afd(afd_direct, string)))
    t1 = time.perf_counter()
    print("Time elapsed: {}s".format(t1 - t0))

