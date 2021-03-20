from graphviz import Digraph
from tree import Node, initial_node
from automaton import State, Transition, AF
from thompson import process
from subset import create_afd
from direct import find_tree_values, create_direct_afd
from simulation import simulate_afd

rules = '(a|b)abb'

print('\n---Creando arbol---\n')

tree, alphabet = Node.initialize_tree(rules)

tree.graph_tree('Arbol', 'Arbol - {}'.format(rules))

#---------------------------------------------------------

print('\n---Creando AFN por metodo de Thompson---\n')

#ARREGLAR
current_node = initial_node(tree)

current_node = current_node.parent

current_state_id = 0

fsm = process(current_node)

fsm.assign_state_numbers()
fsm.graph_fsm('AFN', 'AFN - {}'.format(rules))

#---------------------------------------------------------------

fsm_d = create_afd(fsm, alphabet)
fsm_d.assign_state_numbers()
fsm_d.graph_fsm('AFD', 'AFD - {}'.format(rules))

#--------------------------------------------------------------

new_tree, symbol_ids = find_tree_values(tree)
new_tree.graph_tree('Arbol_Directo', 'Arbol Directo - {}'.format(rules),show_pos=True)

afd_direct = create_direct_afd(new_tree,symbol_ids,alphabet)
afd_direct.assign_state_numbers()
afd_direct.graph_fsm('AFD_directo', 'AFD Directo - {}'.format(rules))

while(True):
    string = input('Ingrese cadena a evaluar: ')
    print(simulate_afd(afd_direct, string))

