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

def s_afn(afn, string, current_index, current_state):
    for i in range(current_index, len(string)):
        found = False
        for transition in afn.transitions:
            if(transition.symbol == string[i] and transition.current_state == current_state):
                current_state = transition.next_state
                found = True
                s_afn()
        if(not found):
            return False

    if(current_state in afn.final_states):
        return True
    else:
        return False

def simulate_afn(afn, string):
    current_state = afn.initial_state

    for i in range(len(string)):
        found = False
        for transition in afn.transitions:
            if(transition.symbol == string[i] and transition.current_state == current_state):
                current_state = transition.next_state
                found = True
        if(not found):
            return False

    if(current_state in afn.final_states):
        return True
    else:
        return False