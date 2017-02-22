import nltk
import sys
from nltk.corpus import cmudict
import string
from pkl_help import *

stress_dictionary = {"word": "1"}
ryhme_dictionary = {}
cluster_dictionary = {}
prondict = cmudict.dict()
not_in_dict = []

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
                print "ERROR: " + word + " NOT IN DICTIONARY!!!"
                not_in_dict.append(word)
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
                stress += '1'

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
                print "ERROR: " + word + " NOT IN DICTIONARY!!!"
                not_in_dict.append(word)
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
        y = string.split(line, " ")
        for x in y:
            lastStressedToEnd(x)
    file.close()
    file = open("data/spenser.txt", 'r')
    for line in file:
        y = string.split(line, " ")
        for x in y:
            lastStressedToEnd(x)
    file.close()
    return cluster_dictionary
def getStresses():
    '''
    Returns stress dictionary
    '''
    return stress_dictionary

def main(argv):

    cluster_dictionary = read_make_pkl("saved_objs/ryhme_dictionary.pkl",
                  lambda: builddictionary())
    stress_dictionary = read_make_pkl("saved_objs/stress_dictionary.pkl",
                  lambda: getStresses())

    # print RhymeWith("cease")
    
if __name__ == "__main__":
    main(sys.argv[1:])