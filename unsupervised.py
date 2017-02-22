# unsupervised.py
from baum_welch import HMM
from pkl_help import *

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

def lines_words_to_lines_ids(line_words, word_to_id):
    '''
    input:
      line_words: list of lists [line_idx][word_idx] = 'word'
      word_to_id: dictionary word_to_id[word] = id
    output: list of lists [line_idx][word_idx] = id
    '''
    id_data = []
    for words in line_words:
        ids = []
        for word in words:
            ids.append(word_to_id[word])
        id_data.append(ids)
    return id_data
        
# TODO(jg):
def make_unsupervised_model(filename, n_states, n_iters):
    '''
    Do unsupervised learning
    returns: an HMM model
    '''
    lines_words = load_poems(filename)
    words = [word for line in lines_words for word in line]
    word_to_id = assign_ids(words)
    lines_ids = lines_words_to_lines_ids(lines_words, word_to_id)
    hmm = HMM.unsupervised_HMM(lines_ids, n_states, n_iters)
    return hmm

def test_unsupervised_py():
    lines_words = load_poems("data/shakespeare.txt")
    # print ("*************************************")
    # print ("lines_words:*************************")
    # print ("*************************************")
    # print lines_words[:4]
    words = [word for line in lines_words for word in line]
    word_to_id = assign_ids(words)
    # print ("*************************************")
    # print ("word_to_id:*************************")
    # print ("*************************************")
    #print word_to_id
    #print ("len(word_to_id): " + str(len(word_to_id)))
    lines_ids = lines_words_to_lines_ids(lines_words, word_to_id)
    # print ("*************************************")
    # print ("lines_ids:*************************")
    # print ("*************************************")
    # print lines_ids[100:106]
    
if __name__ == "__main__":
    model = (
    read_make_pkl("saved_objs/um_shakespeare_nstates25_niters10.pkl",
                  lambda: make_unsupervised_model
                            ("data/shakespeare.txt",
                             25,
                             10))
        )
    

