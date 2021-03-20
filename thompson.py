from graphviz import Digraph
from automaton import State, Transition, AF
from statics import epsilon_symbol, extended_symbols, concat_symbol

current_state_id = 0

def create_or_fsm(fsm_s, fsm_t):
    #ARREGLAR
    global current_state_id
    si = State(current_state_id)
    current_state_id += 1
    sf = State(current_state_id)
    current_state_id += 1

    states = [si,sf]
    states += fsm_s.states + fsm_t.states
    
    transitions = fsm_s.transitions + fsm_t.transitions
    transitions.append(Transition(si, fsm_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, fsm_t.initial_state,epsilon_symbol))
    
    for final_state in fsm_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
    for final_state in fsm_t.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))

    new_fsm = AF()
    new_fsm.states = states
    new_fsm.initial_state = si
    new_fsm.final_states = [sf]
    new_fsm.transitions = transitions
    return new_fsm

def create_clean_closure_fsm(fsm_s):
    #ARREGLAR
    global current_state_id
    si = State(current_state_id)
    current_state_id += 1
    sf = State(current_state_id)
    current_state_id += 1

    states = [si,sf]
    states += fsm_s.states
    
    transitions = fsm_s.transitions
    transitions.append(Transition(si, fsm_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, sf,epsilon_symbol))
    
    for final_state in fsm_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
        transitions.append(Transition(final_state, fsm_s.initial_state, epsilon_symbol))

    new_fsm = AF()
    new_fsm.states = states
    new_fsm.initial_state = si
    new_fsm.final_states = [sf]
    new_fsm.transitions = transitions
    return new_fsm

def create_positive_closure_fsm(fsm_s):
    #ARREGLAR
    global current_state_id
    si = State(current_state_id)
    current_state_id += 1
    sf = State(current_state_id)
    current_state_id += 1

    states = [si,sf]
    states += fsm_s.states
    
    transitions = fsm_s.transitions
    transitions.append(Transition(si, fsm_s.initial_state,epsilon_symbol))
    
    for final_state in fsm_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))
        transitions.append(Transition(final_state, fsm_s.initial_state, epsilon_symbol))

    new_fsm = AF()
    new_fsm.states = states
    new_fsm.initial_state = si
    new_fsm.final_states = [sf]
    new_fsm.transitions = transitions
    return new_fsm

def create_zero_or_one_fsm(fsm_s):
    #ARREGLAR
    global current_state_id
    si = State(current_state_id)
    current_state_id += 1
    sf = State(current_state_id)
    current_state_id += 1

    states = [si,sf]
    states += fsm_s.states
    
    transitions = fsm_s.transitions
    transitions.append(Transition(si, fsm_s.initial_state,epsilon_symbol))
    transitions.append(Transition(si, sf,epsilon_symbol))
    
    for final_state in fsm_s.final_states:
        transitions.append(Transition(final_state, sf,epsilon_symbol))

    new_fsm = AF()
    new_fsm.states = states
    new_fsm.initial_state = si
    new_fsm.final_states = [sf]
    new_fsm.transitions = transitions
    return new_fsm

def create_concat_fsm(fsm_s, fsm_t):
    states = []

    for state in fsm_s.states:
        if(state not in fsm_s.final_states):
            states.append(state)

    states += fsm_t.states
    
    transitions = []
    for transition in fsm_s.transitions:
        if(transition.next_state in fsm_s.final_states):
            transition.next_state = fsm_t.initial_state
        transitions.append(transition)

    transitions += fsm_t.transitions

    new_fsm = AF()
    new_fsm.states = states
    new_fsm.initial_state = fsm_s.initial_state
    new_fsm.final_states = fsm_t.final_states
    new_fsm.transitions = transitions
    return new_fsm

def create_letter_fsm(letter):
    global current_state_id
    si = State(current_state_id)
    current_state_id += 1
    sf = State(current_state_id)
    current_state_id += 1

    transitions = []
    transitions.append(Transition(si,sf,letter))
    
    new_fsm = AF()
    new_fsm.states = [si,sf]
    new_fsm.initial_state = si
    new_fsm.final_states = [sf]
    new_fsm.transitions = transitions
    return new_fsm


def process_down(node):
    fsm = None
    if(node.data in extended_symbols):
        if(node.left.data in extended_symbols):
            fsm_s = process_down(node.left)
        else:
            fsm_s = create_letter_fsm(node.left.data)

        if(node.right):
            if(node.right.data in extended_symbols):
                fsm_t = process_down(node.right)
            else:
                fsm_t = create_letter_fsm(node.right.data)

        if(node.data == '|'):
            print('Creating OR AFN')
            fsm = create_or_fsm(fsm_s,fsm_t)
        elif(node.data == concat_symbol):
            print('Creating CONCAT AFN')
            fsm = create_concat_fsm(fsm_s,fsm_t)
        elif(node.data == '*'):
            print('Creating CLEAN CLOSURE AFN')
            fsm = create_clean_closure_fsm(fsm_s)
        elif(node.data == '+'):
            print('Creating POSITIVE CLOSURE AFN')
            fsm = create_positive_closure_fsm(fsm_s)
        elif(node.data == '?'):
            print('Creating ZERO OR ONE AFN')
            fsm = create_zero_or_one_fsm(fsm_s)
    
    return fsm

def process(node):
    next_node = node
    fsm = None
    while(next_node.data):
        fsm = process_down(next_node)
        if(next_node.parent):
            next_node = next_node.parent
        else:
            break

    return fsm