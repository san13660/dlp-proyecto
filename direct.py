from statics import concat_symbol, epsilon_symbol
from tree import Node
from automaton import State, Transition, AF

def find_node_stuff(node, symbol_ids):
    if(node.is_leaf()):
        if(node.data == epsilon_symbol):
            node.nullable = True
        else:
            node.nullable = False
            node.assign_symbol_id()
            symbol_ids.append({
                'id':node.symbol_id,
                'symbol':node.data
            })
            node.first_pos = {node.symbol_id}
            node.last_pos = {node.symbol_id}
    else:
        if(len(node.left.first_pos) == 0):
            find_node_stuff(node.left, symbol_ids)
        if(node.right and len(node.right.first_pos) == 0):
            find_node_stuff(node.right, symbol_ids)

        if(node.data == concat_symbol):
            if(node.left.nullable and node.right.nullable):
                node.nullable = True

            node.first_pos.update(node.left.first_pos)
            if(node.left.nullable):
                node.first_pos.update(node.right.first_pos)

            node.last_pos.update(node.right.last_pos)
            if(node.right.nullable):
                node.last_pos.update(node.left.last_pos)
        elif(node.data in '*?'):
            node.nullable = True
            node.first_pos.update(node.left.first_pos)
            node.last_pos.update(node.left.last_pos)
        elif(node.data == '+'):
            node.first_pos.update(node.left.first_pos)
            node.last_pos.update(node.left.last_pos)
        elif(node.data == '|'):
            if(node.left.nullable or node.right.nullable):
                node.nullable = True

            node.first_pos.update(node.left.first_pos)
            node.first_pos.update(node.right.first_pos)

            node.last_pos.update(node.left.last_pos)
            node.last_pos.update(node.right.last_pos)

def recursive(afd_direct, current_state, alphabet, symbol_ids, follow_pos_table, final_state_symbol_id):
    for letter in alphabet:
        new_state_id = set()

        for symbol_id in symbol_ids:
            if(symbol_id['symbol'] == letter and symbol_id['id'] in current_state.id):
                new_state_id.update(follow_pos_table[symbol_id['id']])
                print('S:{}   I:{}   IDS:{}'.format(current_state.id, symbol_id['symbol'], new_state_id))

        if(len(new_state_id)==0):
            continue
    
        found_state = None
        for state in afd_direct.states:
            if(state.id == new_state_id):
                found_state = state
                break

        if(found_state):
            afd_direct.transitions.append(Transition(current_state,found_state,letter))
        else:
            new_state = State(new_state_id)
            afd_direct.states.append(new_state)
            afd_direct.transitions.append(Transition(current_state,new_state,letter))

            if(final_state_symbol_id in new_state_id):
                afd_direct.final_states.append(new_state)

            recursive(afd_direct,new_state,alphabet,symbol_ids,follow_pos_table,final_state_symbol_id)

def find_tree_values(tree):
    new_tree = Node(-1, None, data=concat_symbol, left=tree)
    new_tree.right = Node(-2, new_tree, data='#')

    symbol_ids = []
    find_node_stuff(new_tree, symbol_ids)

    return new_tree, symbol_ids

def create_direct_afd(tree, symbol_ids, alphabet):
    follow_pos_table = {}

    final_state_symbol_id = -1

    for symbol_id in symbol_ids:
        follow_pos_table[symbol_id['id']] = set()
        if(symbol_id['symbol'] == '#'):
            final_state_symbol_id = symbol_id['id']

    current_node = tree
    while(current_node):
        for symbol_id in symbol_ids:
            if(current_node.data == concat_symbol and symbol_id['id'] in current_node.left.last_pos):
                follow_pos_table[symbol_id['id']].update(current_node.right.first_pos)

            if(current_node.data == '*' and symbol_id['id'] in current_node.last_pos):
                follow_pos_table[symbol_id['id']].update(current_node.first_pos)
            
        current_node = current_node.left

    print('\n---------------------------')
    print(follow_pos_table)

    afd_direct = AF()

    initial_state = State(tree.first_pos)
    afd_direct.states.append(initial_state)
    afd_direct.initial_state = initial_state

    current_state = initial_state

    recursive(afd_direct,current_state,alphabet,symbol_ids,follow_pos_table,final_state_symbol_id)

    return afd_direct
