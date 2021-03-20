from graphviz import Digraph
from tree import Node, initial_node
from automaton import State, Transition, AF
from thompson import process
from subset import create_afd
from direct import find_tree_values, create_direct_afd
from simulation import simulate_afd, simulate_afn

import time

rules = '(εa|εb)*abb'

print('\n---Creando arbol---\n')

tree, alphabet = Node.initialize_tree(rules)

tree.graph_tree('Arbol', 'Arbol - {}'.format(rules))

#---------------------------------------------------------

print('\n---Creando AFN por metodo de Thompson---\n')

#ARREGLAR
current_node = initial_node(tree)

current_node = current_node.parent

current_state_id = 0

afn = process(current_node)

afn.assign_state_numbers()
afn.graph_fsm('AFN', 'AFN - {}'.format(rules))

#---------------------------------------------------------------

print('\n---Creando AFD por subconjuntos---\n')

afd = create_afd(afn, alphabet)
afd.assign_state_numbers()
afd.graph_fsm('AFD', 'AFD - {}'.format(rules))

#--------------------------------------------------------------

print('\n---Creando AFD por metodo directo---\n')

new_tree, symbol_ids = find_tree_values(tree)
new_tree.graph_tree('Arbol_Directo', 'Arbol Directo - {}'.format(rules),show_pos=True)

afd_direct = create_direct_afd(new_tree,symbol_ids,alphabet)
afd_direct.assign_state_numbers()
afd_direct.graph_fsm('AFD_directo', 'AFD Directo - {}'.format(rules))

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

