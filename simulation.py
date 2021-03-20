from statics import epsilon_symbol

def simulate_afd(afd, string):
    current_state = afd.initial_state

    for s in string:
        found = False
        for transition in afd.transitions:
            if(transition.symbol == s and transition.current_state == current_state):
                current_state = transition.next_state
                found = True
                break
        if(not found):
            return False

    if(current_state in afd.final_states):
        return True
    else:
        return False

def recursive_simulation(afn, string, current_index, current_state, prev_e_states=[]):
    if(current_index == len(string)):
        if(current_state in afn.final_states):
            return True

    for transition in afn.transitions:
        if(transition.current_state == current_state):
            if(transition.symbol == epsilon_symbol):
                if(transition.next_state not in prev_e_states):
                    new_prev_e_states = prev_e_states.copy()
                    new_prev_e_states.append(current_state)
                    if(recursive_simulation(afn, string, current_index, transition.next_state, new_prev_e_states)):
                        return True
            elif(current_index < len(string) and transition.symbol == string[current_index]):
                if(recursive_simulation(afn, string, current_index+1, transition.next_state)):
                    return True
    
    return False

def simulate_afn(afn, string):
    current_state = afn.initial_state

    if(recursive_simulation(afn, string, 0, current_state)):
        return True
    else:
        return False