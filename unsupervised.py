# unsupervised.py
from baum_welch import HMM
from pkl_help import *
from preprocessing import cleanWord

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
            lines_words.append(map(cleanWord, words))
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
        
def make_unsupervised_model(filename, n_states, n_iters):
    '''
    Do unsupervised learning
    returns: an HMM model, dictionary word->id, dictionary id->word
    '''
    lines_words = load_poems(filename)
    words = [word for line in lines_words for word in line]
    word_to_id = assign_ids(words)
    id_to_word = {}
    for key, value in word_to_id.items():
        id_to_word[value] = key
    # DEBUG
    print ("*************************************")
    print ("id_to_word:*************************")
    print ("*************************************")
    print id_to_word
    lines_ids = lines_words_to_lines_ids(lines_words, word_to_id)
    hmm = HMM.unsupervised_HMM(lines_ids, n_states, n_iters)
    return (hmm, word_to_id, id_to_word)

def generate_poem(model, ids_to_words, words_per_line, n_lines):
    lines = []
    for line_idx in range(n_lines):
        line_ids = model.generate_emission_list(words_per_line)
        line_words = [ids_to_words[id] for id in line_ids]
        lines.append(" ".join(line_words))
    return lines

    
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
    model, word_to_id, id_to_word = (
    read_make_pkl("saved_objs/um_all_nstates20_niters1000.pkl",
                  lambda: make_unsupervised_model
                            ("data/shakespeare_plus_spenser.txt",
                             n_states=20,
                             n_iters=1000))
        )
    poem = generate_poem(model, id_to_word, words_per_line=8, n_lines=14)

    print ("*************************************")
    print ("Generated Poem:**********************")
    print ("*************************************")
    for line in poem:
        print line

