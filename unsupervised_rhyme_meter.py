# unsupervised.py
from baum_welch import HMM
from pkl_help import * 
import nltk
import random
from nltk.corpus import cmudict
# import poetrytools

prondict = cmudict.dict()
stress_dictionary = read_make_pkl("saved_objs/stress_dictionary.pkl", lambda: test_unsupervised_py())
rhyme_dictionary = read_make_pkl("saved_objs/ryhme_dictionary.pkl", lambda: test_unsupervised_py())
id_stress = {}
id_rhyme = {}


def justStress(lst):
    '''
    Removes all information from cmudictionary except for stresses. Also makes any secondary stresses
    primary.
    '''
    stresses = ''
    for w in lst:
        for c in list(w):
            if c.isdigit():
                if c == '2':
                    stresses += '1'
                else:
                    stresses += c
    return stresses

def WordToStress(word):
    '''
    Takes in a word, parses the word to just lowercase letters. Checks the working dictionary
    to see if we've already labeled this word. If we haven't, it checks to see if it's in 
    the cmu dictionary - prints an error if it isn't. If it's in the cmu dictionary then we
    get its stresses and remove phonemes.
    '''
    stress = ""
    word = cleanUp(word)

    zero = True
    for x in prondict[word]:
        if isAlternating(justStress(x)):
            stress += justStress(x)
    stress_dictionary[word] = stress
    return stress

def replace2with1(lst):
    '''
    Helper function to replace any secondary stress with primary, used in rhyme matching.
    '''
    for x in range(len(lst)):
        lst[x] = lst[x].replace('2', '1')
    return lst

def cleanUp(word):
    '''
    Removes punctuation from the word given in the parameter, and returns the lowercase
    version of that word.
    '''
    word = word.strip()
    punctuations = '\'!()[]{};:"\,<>./?@#$%^&*_~'
    clean_word = []
    w = ""
    for c in word:
        if c == "-":
            clean_word.append(w.lower())
            w = ""
            continue
        if c not in punctuations:
            w += c
    clean_word.append(w.lower())
    return clean_word

def REVERSED_lines_words_to_lines_ids(line_words, word_to_id):
    '''
    Reverses the word order of each list of words.

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
        reversed(ids)
        id_data.append(ids)
    return id_data

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
            lst = []
            for x in words:
                for y in cleanUp(x):
                    lst.append(y)
            lines_words.append(lst)
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
        
def Rhyme_make_unsupervised_model(filename, n_states, n_iters):
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
    
    lines_ids = REVERSED_lines_words_to_lines_ids(lines_words, word_to_id)
    hmm = HMM.unsupervised_HMM(lines_ids, n_states, n_iters)
    return (hmm, word_to_id, id_to_word)

def syl_so_far(line, word_to_id, id_to_word):
    '''
    Given a list of ids, returns the current number of syl in the line.
    If a word is not in the stress dictionary it guesses 2 syl, but this 
    function only works well if we have all the stresses....
    '''
    summ = 0
    for x in line:
        try:
            summ += len(stress_dictionary[id_to_word[x]])
        except:
            summ += 2
    return summ

def RhymingPair(min_number):
    '''
    Param = smallest size of cluster to sample from. Ie we only choose a rhyme cluster if it has
    more members than the min_number.

    This function returns a list of the ending words for each line to match the rhyme pattern.
    This function is made specifically for the sonnet rhyming pattern, would need to be altered
    for other poem types.
    '''
    lst = ["" for _ in range(14)]
    for l in range(7):
        x = ()
        while True:
            x = random.choice(rhyme_dictionary.keys())
            if len(rhyme_dictionary[x]) >= min_number:
                break
        a = "1"
        b = "1"
        while a == b:   
            a = random.choice(rhyme_dictionary[x])
            b = random.choice(rhyme_dictionary[x])
            try:
                if(stress_dictionary[a][0] == "0"):
                    a = b
                    continue
            except:
                while True:
                        x = random.choice(rhyme_dictionary.keys())
                        if len(rhyme_dictionary[x]) >= min_number:
                            break
                continue
        if l < 2:
            lst[l] = a
            lst[l+2] = b
        elif l < 4:
            lst[2+l] = a
            lst[l+4] = b
        elif l < 6:
            lst[l+4] = a
            lst[l+6] = b
        else:
            lst[12] = a
            lst[13] = b
    return lst 

def isAlternating(str1):
    start = str1[0]
    for x in str1[1:]:
        if x == start:
            return False
        start = x
    return True    

def generate_rhyming_poem(model, ids_to_words, word_to_id):
    '''
    Requries model to be trained backwards!
    '''
    rhyme = RhymingPair(4)
    # for x in rhyme:
    #     pos(x)
    lines = []
    tails = []
    for line_idx in range(14):
        print "Line ", line_idx
        line_ids = []
        index = 0
        line_ids += [word_to_id[rhyme[line_idx]]]
        # model.generate_emission_list_start(pos_to_id[pos_dictionary[rhyme[line_idx]]], line_idx, index)
        index += 1
        stress = ""
        backtrace = False
        counter = 0
        while True:
            # Incase we get stuck in a bad state - start from rhyme word.
            if counter == 100:
                index = 2
                backtrace = True
                line_ids = [line_ids[0]]
                print "restarting this line"
                counter = 0
                continue
            counter += 1
            # Get previous words first syl
            try:
                stress = stress_dictionary[id_to_word[line_ids[-1]]][0]
            except:
                del line_ids[-1]
                index -= 1
                backtrace = True
                continue
            # If backtrace == False, new query, if backtrace == True, requring a previous state.
            line_ids += model.generate_emission_list(1, backtrace, line_idx, index)
            index += 1
            # Try to see if we have the stresses for this word, if we don't resample
            try:
                stress_dictionary[id_to_word[line_ids[-1]]]
            except:
                del line_ids[-1]
                index -= 1
                backtrace = True
                continue
            # If this word doesn't have an alternating stress pattern, check to see if has
            # another pronounciation, if not resample.
            if(not isAlternating(stress_dictionary[id_to_word[line_ids[-1]]])):
                if(justStress(id_to_word[line_ids[-1]]) == ""):
                    if(index > 4):
                        del line_ids[-1]
                        del line_ids[-1]
                        del line_ids[-1]
                        index -= 3
                        backtrace = True
                        continue
            # If end of the current word matches the stress of the last of the previous word
            # get ride of this word and resample
            if(stress_dictionary[id_to_word[line_ids[-1]]][-1] == stress):
                del line_ids[-1]
                index -= 1
                backtrace = True
                continue
            # If we have 10 syl, make sure we are starting unstressed. If not resample.
            if (syl_so_far(line_ids, word_to_id, ids_to_words) == 10):
                if(stress_dictionary[id_to_word[line_ids[-1]]][0] == "0"):
                    break
                else:
                    del line_ids[-1]
                    del line_ids[-1]
                    del line_ids[-1]
                    backtrace = True
                    index -= 3
                    continue
            # If we have more than 10 syl, ditch the last 3 words and re sample
            if (syl_so_far(line_ids, word_to_id, ids_to_words) >= 10):
                del line_ids[-1]
                del line_ids[-1]
                del line_ids[-1]
                backtrace = True
                index -= 3
                continue
            backtrace = False

        # reverse the words since we trained backwards
        line_ids = reversed(line_ids)
        # Convert list of ids to actual words
        line_words = [ids_to_words[id] for id in line_ids]
        # Put into string with space splicing
        lines.append(" ".join(line_words).capitalize().replace(" i ", " I "))
        # Capitalizes first letter and I's
    return lines
    
if __name__ == "__main__":
    model, word_to_id, id_to_word = (
    read_make_pkl("saved_objs/um_shakespeare_nstates30_niters750.pkl",
                  lambda: Rhyme_make_unsupervised_model("data/shakespeare.txt", 25, 1000))
        )
    poem = generate_rhyming_poem(model, id_to_word, word_to_id)

    print ("*************************************")
    print ("Generated Poem:**********************")
    print ("*************************************")
    counter = 0
    # Alternates commas and periods for punctuation...
    # Could probably do better....
    # If we could use a little supervised learning we could do this with Naive Bayes
    #               P(Punctuation|word) and sample, include nothing as an option (most common)
    for line in poem:
        if counter % 2 == 0:
            print line + ","
        else:
            print line.capitalize().replace(" i ", " I ") + "."
        counter += 1
    # Prints syl stresses
    print "      -----------------------------------------------------------------"
    counter = 1
    for line in poem:
        lst = ""
        if counter < 10:
            print " Line  ", counter, ": ",
        else:
            print " Line ", counter, ": ",
        for x in line.split():
            try: 
                print stress_dictionary[x] + " ",
                lst += stress_dictionary[x]
            except:
                print "  ",
        print "\t: SUM -> ", len(lst)
        counter += 1