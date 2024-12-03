import csv
from collections import deque

def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        machine_name = next(reader)[0]
        states = next(reader)[0].split(',')
        alphabet = next(reader)[0].split(',')
        tape_symbols = next(reader)[0].split(',')
        start_state = next(reader)[0]
        accept_state = next(reader)[0]
        reject_state = next(reader)[0]
        transitions = {}
        
        for row in reader:
            if not row:
                continue
            state, char, next_state, write_char, move_dir = row
            transitions.setdefault((state, char), []).append((next_state, write_char, move_dir))
    
    return {
        'name': machine_name,
        'states': states,
        'alphabet': alphabet,
        'tape_symbols': tape_symbols,
        'start_state': start_state,
        'accept_state': accept_state,
        'reject_state': reject_state,
        'transitions': transitions
    }

def simulate_ntm(machine, input_string, max_depth=None):
    print(f'Running machine -  {machine["name"]}\nstring -  {input_string}')
    start_config = (machine['start_state'], input_string, 0)  # (state, tape, head_pos)
    tree = [[start_config]]
    transitions = machine['transitions']
    accept_state = machine['accept_state']
    reject_state = machine['reject_state']

    total_transitions = 0
    non_leaves = 0
    transition_log = []

    for depth in range(max_depth or float('inf')):
        current_level = tree[-1]
        next_level = []

        for state, tape, head_pos in current_level:
            if state == accept_state:
                print(f"String accepted in {depth} steps.")
                print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}")
                print("Transition Log:")
                for log in transition_log:
                    print(log)
                return True
            if state == reject_state:
                print("rejected")
                continue
            
            head_char = tape[head_pos] if 0 <= head_pos < len(tape) else '_'
            possible_transitions = transitions.get((state, head_char), [])
            
            # Track nondeterministic nodes
            if len(possible_transitions) > 1:
                non_leaves += 1
            
            for next_state, write_char, move_dir in possible_transitions:
                new_tape = list(tape)
                if 0 <= head_pos < len(new_tape):
                    new_tape[head_pos] = write_char
                else:
                    new_tape.append(write_char)
                
                new_head_pos = head_pos + (1 if move_dir == 'R' else -1)
                next_config = (next_state, ''.join(new_tape), new_head_pos)
                next_level.append(next_config)

                # Log transition
                transition_log.append(
                    f"({state}, {head_char}) -> ({next_state}, {write_char}, {move_dir})"
                )

            total_transitions += len(possible_transitions)
        
        if not next_level:
            print(f"String rejected in {depth} steps.")
            print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}")
            print("Transition Log:")
            for log in transition_log:
                print(log)
            return False
        
        tree.append(next_level)
    
    print(f"Execution stopped after reaching max depth of {max_depth}.")
    print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}")
    print("Transition Log:")
    for log in transition_log:
        print(log)
    return None

# Example Usage
machine_file = 'test/a_plus.csv'
input_string = 'aaaa'
max_depth = 20

machine = parse_csv(machine_file)
simulate_ntm(machine, input_string, max_depth)

