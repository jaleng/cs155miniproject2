# visualize.py
from baum_welch import HMM
from pkl_help import *
import sys
import networkx as nx
import matplotlib.pyplot as plt

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

def find_state_imp_words(model, state, id_to_word, n_imp_words):
    max_emission_probs = []
    probs_cpy = list(model.O[state])
    prev_max = -1.
    chosen_words = []
    for _ in range(n_imp_words):
        curr_max = max(probs_cpy)
        # Assuming this won't happen for simplicity, if it does must fix.
        if curr_max == prev_max:
            raise Exception('Duplicate values when finding top words')
        prev_max = curr_max
        max_emission_probs.append(curr_max)
        chosen_words.append(id_to_word[model.O[state].index(curr_max)])
        probs_cpy.remove(curr_max)
    return chosen_words
    
def make_graph(model, states):
    dg = nx.DiGraph()
    for s1 in states:
        for s2 in states:
            dg.add_edge(s1, s2, weight=model.A[s1][s2])
    return dg
            
def draw_graph(dg, filename):
    labels = nx.get_edge_attributes(dg, 'weight')
    for key, value in labels.items():
        new_val = '{:2.2f}'.format(value)
        if new_val == '0.00':
            new_val = '0'
        labels[key] = new_val
    #print("labels: " + str(labels))
    pos = nx.spring_layout(dg)
    nx.draw_networkx_nodes(dg, pos=pos, alpha=0.5)
    nx.draw_networkx_labels(dg, pos=pos, alpha=0.5, font_size=20)
    for edge, weight in labels.items():
        nx.draw_networkx_edges(dg, pos=pos, edgelist=[edge], width=10*float(weight))
    #nx.draw_networkx_edges(dg, pos=pos, alpha=0.5)
    nx.draw_networkx_edge_labels(dg, pos=pos, edge_labels=labels,
                                 alpha=1., label_pos=0.25)
    plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    model, word_to_id, id_to_word = (
        get_pkl("saved_objs/um_all_nstates20_niters1000.pkl")
        )
    imp_states = find_important_states(model, 5)
    print ("imp_states: " + str(imp_states))
    for state in imp_states:
        print ("words for state "
               + str(state) + ": "
               + str(find_state_imp_words(model, state, id_to_word, 5)))
    draw_graph(make_graph(model, imp_states), "graphs/test.pdf")
     
    
