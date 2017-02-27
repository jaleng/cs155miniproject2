# visualize.py
from baum_welch import HMM
from pkl_help import *
import sys

def find_important_states(model, n_chosen_states):
    '''
    Find most transitioned-to states
    '''
    n_states = model.L
    state_prob_sums = [0. for _ in range(n_states)]
    for s1 in range(n_states):
        for s2 in range(n_states):
            state_prob_sums[s2] += model.A[s1][s2]
    sums_cpy = list(state_prob_sums)
    maxes = []
    chosen_states = []
    prev_max = -1.
    for _ in range(n_chosen_states):
        curr_max = max(sums_cpy)
        # Assuming this won't happen for simplicity, if it does must fix.
        if curr_max == prev_max:
            raise Exception('Duplicate prob sums when finding top states')
        prev_max = curr_max
        maxes.append(max(sums_cpy))
        chosen_states.append(state_prob_sums.index(curr_max))
        sums_cpy.remove(curr_max)
    return chosen_states

if __name__ == "__main__":
    model, word_to_id, id_to_word = (
        get_pkl("saved_objs/um_shakespeare_nstates6_niters10000.pkl")
        )
    imp_states = find_important_states(model, 5)
    print ("imp_states: " + str(imp_states))
     
    
