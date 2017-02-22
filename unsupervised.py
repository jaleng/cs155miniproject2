# unsupervised.py

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
    curr_id = 0
    word_to_id = {}
    for word in words:
        if word not in word_to_id:
            word_to_id[word] = curr_id
            curr_id += 1
    return word_to_id

# TODO(jg):
def make_unsupervised_model(n_states):
    '''
    Do unsupervised learning
    returns: an HMM model
    '''
    pass

if __name__ == "__main__":
    lines_words = load_poems("data/shakespeare.txt")
    # print ("*************************************")
    # print ("lines_words:*************************")
    # print ("*************************************")
    # print lines_words[:4]
    words = [word for line in lines_words for word in line]
    word_to_id = assign_ids(words)
    print ("*************************************")
    print ("word_to_id:*************************")
    print ("*************************************")
    #print word_to_id
    print ("len(word_to_id): " + str(len(word_to_id)))
