import nltk
import sys
from nltk.corpus import cmudict
from nltk.corpus import brown
import string
from pkl_help import *

prondict = cmudict.dict()
# stress_dictionary = {}
stress_dictionary = read_make_pkl("saved_objs/stress_dictionary.pkl",
                  lambda: getStresses())
ryhme_dictionary = {}
cluster_dictionary = read_make_pkl("saved_objs/ryhme_dictionary.pkl",
                  lambda: builddictionary())
prondict = cmudict.dict()
not_in_dict = []
pos_dictionary = {}
# brown_tagged_sents = brown.tagged_sents(categories='romance')
# unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)

# def pos(word):
#     part = ''
#     # print word
#     word = nltk.word_tokenize(word.lower())

#     if(word in pos_dictionary.keys()):
#         return pos_dictionary[word]
#     else:
#         # try:
#         part_of_speech = nltk.pos_tag(word)
#         # print part_of_speech
#         part = part_of_speech[0][1]
#         # print word + ": " + str(part)
#         if part == None:
#             return ''
#         pos_dictionary[part_of_speech[0][0]] = part
#         return part
#         # except:
#         #     print "issue."
#         #     return part

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
            # lines_words.append(lst)
    return

def cleanWord(word):
    '''
    Removes punctuation from the word given in the parameter, and returns the lowercase
    version of that word.
    '''
    word = word.strip()
    punctuations = '\'!()[]{};:"\,<>./?@#$%^&*_~'
    clean_word = ""
    for c in word:
        if c not in punctuations:
            clean_word += c
    return clean_word.lower()

def cleanUp(word):
    '''
    Removes punctuation from the word given in the parameter, and returns the lowercase
    version of that word.
    '''
    word = word.strip()
    punctuations = '\'!()[]{};:"\,<>./?@#$%^&*_~'
    clean_word = ""
    for c in word:
        if c == "-":
            WordToStress(clean_word.lower())
            clean_word = ""
            continue
        if c not in punctuations:
            clean_word += c
    return clean_word.lower()

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

def replace2with1(lst):
    '''
    Helper functino to replace any secondary streses with primary, used in rhyme matching.
    '''
    for x in range(len(lst)):
        lst[x] = lst[x].replace('2', '1')
    return lst

def WordToStress(word):
    '''
    Takes in a word, parses the word to just lowercase letters. Checks the working dictionary
    to see if we've already labeled this word. If we haven't, it checks to see if it's in 
    the cmu dictionary - prints an error if it isn't. If it's in the cmu dictionary then we
    get its stresses and remove phonemes.
    '''
    stress = ""
    word = cleanUp(word)
    if word in stress_dictionary.keys():
        # print word + " is in the dictionary!"
        return stress_dictionary[word]
    else:
        if word not in prondict:
            if(word != ''):
                # print "ERROR: " + word + " NOT IN DICTIONARY!!!"
                
                return ""
        else:
            zero = True
            for x in prondict[word]:

                if justStress(x) == "0":
                    stress += "0"
                    zero = False
                    break
            if zero:
                stress += justStress(prondict[word][0])
            if (stress.endswith('100')):
                stress = stress[:-1]
                # EX every ; 100 -> 10

            stress_dictionary[word] = stress
    return stress

def lastStressedToEnd(word):
    '''
    Takes in a word and cleans it. Then gets the phonemes for the word from the last
    stressed vowel to end (this must match for a word to be a strict rhyme), and
    sorts it into the dictionary according to it's ending.
    '''
    word = cleanUp(word)
    lst = []
    if word in ryhme_dictionary.keys():
        # print word + " is in the dictionary!"
        
        lst = ryhme_dictionary[word]
        return lst
    else:
        if word not in prondict:
            if(word != ''):
                return lst
                # print "ERROR: " + word + " NOT IN DICTIONARY!!!"
                # not_in_dict.append(word)
        else:
            lst = prondict[word][0]
            stresses = list(WordToStress(word))
            index = ''.join(stresses).rfind('1')
            
            if(index > 0):
                for x in range(int(index)):
                    while(True):
                        if (justStress(lst[0]) == ""):
                            del lst[0]
                            continue
                        del lst[0]
                        break
            while True:
                if (justStress(lst[0]) == ""):
                    del lst[0]
                else:
                    break
            lst = replace2with1(lst)
            ryhme_dictionary[word] = lst
            if(tuple(lst) not in cluster_dictionary.keys()):
                cluster_dictionary[tuple(lst)] = [word]
            else:
                cluster_dictionary[tuple(lst)].append(word)
        return lst
def interpolateStress(word, line):
    '''
    Interpolates the stresses of word not in dictionary.
    Only works if one word in line is unknown.
    '''
    number_not_dict = 0
    # print stress_dictionary
    for x in line:
        x = cleanUp(x)
        if x not in stress_dictionary.keys() and len(x) > 1:
            number_not_dict += 1
    if number_not_dict > 1:
        not_in_dict.append(word)
        # print "More than 1 word not in dictionary."
        return
    sum_of_syl = 0
    stress = ""
    first = ""
    second = ""
    index = -1
    for x in line:
        if x == word:
            continue
        sum_of_syl += len(WordToStress(x))
    index = line.index(word)
    if index == 0:
        stress += "1"
        for x in range(10 - sum_of_syl - 1):
            if x % 2 == 0:
                stress += "0"
            else:
                stress += "1"
    elif index == (len(line) - 1):
        prev_stress = WordToStress(line[index - 1])[-1]
        if(prev_stress == "0"):
            first = "1"
            second = "0"
        else:
            first = "0"
            second = "1"
        for x in range(10 - sum_of_syl - 1):
            if x % 2 == 0:
                stress += first
            else:
                stress += second
        stress += "0"
    else:
        prev_stress = WordToStress(line[index - 1])[-1]
        post_stress = WordToStress(line[index + 1])[0]
        if(prev_stress == "0"):
            first = "1"
            second = "0"
        else:
            first = "0"
            second = "1"
        for x in range(10 - sum_of_syl):
            if x % 2 == 0:
                stress += first
            else:
                stress += second
    # print "Guess for " + word + ": " + stress
    stress_dictionary[word] = stress

def RhymeWith(word):
    '''
    Takes in a word, returns a list of rhymes that were found in the txts.
    '''
    ending = lastStressedToEnd(word)
    return cluster_dictionary[tuple(ending)]

def builddictionary():
    '''
    Builds both the stress and rhyme dictionaries. Stress dictionary is 
    required to build the rhyme dictionary. This function returns the ryhme dictionary
    '''
    file = open("data/shakespeare.txt", 'r')
    for line in file:
        y = line.strip()
        y = y.split()
        for x in y:
            lastStressedToEnd(x)
            pos(x)
    file.close()
    file = open("data/spenser.txt", 'r')
    for line in file:
        y = line.strip()
        y = y.split()
        for x in y:
            lastStressedToEnd(x)
            pos(x)
    file.close()
    return cluster_dictionary

def build_pos_dictionary(filename):
    '''
    Builds both the stress and rhyme dictionaries. Stress dictionary is 
    required to build the rhyme dictionary. This function returns the ryhme dictionary
    '''
    with open(filename) as f:
        for line in f:
            line = line.strip()
            words = line.split()
            if len(words) <= 1:
                continue
            lst = []
            for x in words:
                for y in cleanUp(x):
                    pos(y)
    return pos_dictionary
def getStresses(filename):
    '''
    Returns stress dictionary
    '''
    file = open(filename, 'r')
    for line in file:
        y = line.strip()
        y = y.split()
        if len(y) <= 1:
                continue
        for x in y:
            n = WordToStress(x)
            if(n == ""):
                interpolateStress(x, y)
    return stress_dictionary

def main(argv):

    # interpolateStress("doth", ["he", "lovely", "gaze", "where", "every", "eye", "doth", "dwell"])
    # print stress_dictionary["fawn"]
    # dic = read_make_pkl("saved_objs/stress_dictionary.pkl",
    #               lambda: getStresses("data/shakespeare.txt"))

if __name__ == "__main__":
    main(sys.argv[1:])
