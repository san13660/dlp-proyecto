from graphviz import Digraph
from automaton import State, Transition, AF
from statics import epsilon_symbol, extended_symbols, concat_symbol

def create_or_fsm(afn, afn_s, afn_t):
    
    si = afn.create_state()
    sf = afn.create_state()

    states = [si,sf]
    states += afn_s.states + afn_t.states
    
    transitions = afn_s.transitions + afn_t.transitions
    transitions.append(Transition(si, afn_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, afn_t.initial_state,epsilon_symbol))
    
    for final_state in afn_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
    for final_state in afn_t.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))

    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = states
    new_afn.initial_state = si
    new_afn.final_states = [sf]
    new_afn.transitions = transitions
    return new_afn

def create_clean_closure_fsm(afn, afn_s):
    si = afn.create_state()
    sf = afn.create_state()

    states = [si,sf]
    states += afn_s.states
    
    transitions = afn_s.transitions
    transitions.append(Transition(si, afn_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, sf,epsilon_symbol))
    
    for final_state in afn_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
        transitions.append(Transition(final_state, afn_s.initial_state, epsilon_symbol))

    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = states
    new_afn.initial_state = si
    new_afn.final_states = [sf]
    new_afn.transitions = transitions
    return new_afn

def create_positive_closure_fsm(afn, afn_s):
    si = afn.create_state()
    sf = afn.create_state()

    states = [si,sf]
    states += afn_s.states
    
    transitions = afn_s.transitions
    transitions.append(Transition(si, afn_s.initial_state,epsilon_symbol))
    
    for final_state in afn_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
        transitions.append(Transition(final_state, afn_s.initial_state, epsilon_symbol))

    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = states
    new_afn.initial_state = si
    new_afn.final_states = [sf]
    new_afn.transitions = transitions
    return new_afn

def create_zero_or_one_fsm(afn, afn_s):
    si = afn.create_state()
    sf = afn.create_state()

    states = [si,sf]
    states += afn_s.states
    
    transitions = afn_s.transitions
    transitions.append(Transition(si, afn_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, sf,epsilon_symbol))
    
    for final_state in afn_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))

    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = states
    new_afn.initial_state = si
    new_afn.final_states = [sf]
    new_afn.transitions = transitions
    return new_afn

def create_concat_fsm(afn, afn_s, afn_t):
    states = []

    for state in afn_s.states:
        if(state not in afn_s.final_states):
            states.append(state)

    states += afn_t.states
    
    transitions = []
    for transition in afn_s.transitions:
        if(transition.next_state in afn_s.final_states):
            transition.next_state = afn_t.initial_state
        transitions.append(transition)

    transitions += afn_t.transitions

    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = states
    new_afn.initial_state = afn_s.initial_state
    new_afn.final_states = afn_t.final_states
    new_afn.transitions = transitions
    return new_afn

def create_letter_fsm(afn, letter):
    si = afn.create_state()
    sf = afn.create_state()

    transitions = []
    transitions.append(Transition(si,sf,letter))
    
    new_afn = AF(start_node_id=afn.current_node_id)
    new_afn.states = [si,sf]
    new_afn.initial_state = si
    new_afn.final_states = [sf]
    new_afn.transitions = transitions
    return new_afn


def recursive_process_node(afn_o, node):
    if(node.left.data in extended_symbols):
        afn_s = recursive_process_node(afn_o, node.left)
    else:
        afn_s = create_letter_fsm(afn_o, node.left.data)

    if(node.right):
        if(node.right.data in extended_symbols):
            afn_t = recursive_process_node(afn_o, node.right)
        else:
            afn_t = create_letter_fsm(afn_o, node.right.data)

    if(node.data == '|'):
        print('Creating OR AFN')
        afn = create_or_fsm(afn_o, afn_s,afn_t)
    elif(node.data == concat_symbol):
        print('Creating CONCAT AFN')
        afn = create_concat_fsm(afn_o, afn_s,afn_t)
    elif(node.data == '*'):
        print('Creating CLEAN CLOSURE AFN')
        afn = create_clean_closure_fsm(afn_o, afn_s)
    elif(node.data == '+'):
        print('Creating POSITIVE CLOSURE AFN')
        afn = create_positive_closure_fsm(afn_o, afn_s)
    elif(node.data == '?'):
        print('Creating ZERO OR ONE AFN')
        afn = create_zero_or_one_fsm(afn_o, afn_s)
    
    return afn

def create_afn(root):
    afn = AF()
    afn = recursive_process_node(afn, root)
    return afn