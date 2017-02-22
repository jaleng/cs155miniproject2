# unsupervised.py

# TODO(jg):
def load_poems(filename):
    '''
    Load the poetry file into a list [lines] of lists [words]
    X[line_idx][word_idx]
    '''
    lines_words = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            words = line.split()
            if len(words) <= 1:
                continue
            lines_words.append(words)
    return lines_words

# TODO(jg):
def assign_ids(words):
    '''
    Assign each word a unique id [0->#(unique-words - 1)]
    input: list of words
    output: dict{word: id}
    '''
    pass

# TODO(jg):
def make_unsupervised_model(n_states):
    '''
    Do unsupervised learning
    returns: an HMM model
    '''
    pass

if __name__ == "__main__":
    lines_words = load_poems("data/shakespeare.txt")
    print ("*************************************")
    print ("lines_words:*************************")
    print ("*************************************")
    print lines_words[:10]
