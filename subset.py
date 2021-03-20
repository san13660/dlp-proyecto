from graphviz import Digraph
from automaton import State, Transition, AF
from statics import epsilon_symbol, extended_symbols, concat_symbol

def e_closure(afn, state, past_states_ids=set()):
    if(type(state.id) is set):
        state_id_set = state.id.copy()
    else:
        state_id_set = {state.id}

    for transition in afn.transitions:
        if(transition.symbol == epsilon_symbol 
        and transition.current_state.id in state_id_set
        and transition.next_state.id not in state_id_set 
        and transition.next_state.id not in past_states_ids):
            new_past_states_ids = past_states_ids.copy()
            new_past_states_ids.add(transition.next_state.id)
            new_state, _ = e_closure(afn, transition.next_state, new_past_states_ids)
            state_id_set.update(new_state.id)
            
    return State(state_id_set), past_states_ids

def mov(afn, state, letter):
    if(type(state.id) is set):
        state_id_set = state.id.copy()
    else:
        state_id_set = {state.id}

    state_transitions = [transition for transition in afn.transitions if(transition.current_state.id in state_id_set and transition.symbol == letter)]
    new_subset = set()
    for transition in state_transitions:
        new_subset.add(transition.next_state.id)
    
    if(len(new_subset) > 0):
        return State(new_subset)
    else:
        return None
    

def recursive_mov(afn, afd, state, letters):
    for letter in letters:
        new_state = mov(afn, state, letter)
        print('mov({}, {}) = {}'.format(set(state.id),letter,set(new_state.id) if new_state else {}))
        if(new_state):
            new_state_2, _ = e_closure(afn, new_state)
            print('e-closure({}) = {}'.format(set(new_state.id),set(new_state_2.id)))
            new_transitions = Transition(state, new_state_2, letter)

            if(new_transitions not in afd.transitions):
                afd.transitions.append(new_transitions)

            if(new_state_2 not in afd.states):
                afd.states.append(new_state_2)
                recursive_mov(afn, afd, new_state_2, letters)

def create_afd(afn, letters):
    afd = AF()
    
    initial_state, _ = e_closure(afn, afn.initial_state)
    print('e-closure({}) = {}'.format(set([afn.initial_state.id]),set(initial_state.id)))

    afd.states.append(initial_state)
    afd.initial_state = initial_state
    recursive_mov(afn, afd, initial_state, letters)

    for state in afd.states:
        for final_state in afn.final_states:
            if final_state.id in state.id:
                afd.final_states.append(state)

    print('\nTransiciones de AFD')
    for transition in afd.transitions:
        print('{} -{}-> {}'.format(transition.current_state.id, transition.symbol, transition.next_state.id))
    
    return afd
