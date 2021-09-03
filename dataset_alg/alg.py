'''
- Using spaCy’s English pipeline ('en_core_web_lg') trained on written web text (blogs, news, comments), that includes vocabulary, vectors, syntax and entities. Imported as a module (https://spacy.io/models/en#en_core_web_lg);

Example: {'T1': 'A man, the thief, the assailant, The thief'} -> {'T1': 'assailant'}

- Steps from the initial example with a set of ACTOR descriptions to the most specific term:
    
    1 - Convert all uppercase characters to lowercase;

    2 - Lemmatization;

    3 - Clean duplicates;

    4 - Only keep words with NOUN Synsets (different senses of a particular word/synonym sets - set of lemmas with related meaning);

    5 - Only keep words with NOUN Lemmas (synonyms within each sense);

    6 - Get a list hypernyms;

    7 - Compare hypernyms with root node;
        Tiebreaker for cases where the hypernyms have the same distance to the root: count hyponyms;

    8 - Similarity between the elements of the list after step 5 and the lowest common hypernym (after step 7).
'''

import nltk
import spacy
import en_core_web_lg
from nltk.corpus import wordnet as wn

nlp = spacy.load('en_core_web_lg')      # load package "en_core_web_lg"

# process dictionary
def filter_actors(dict):
    for key, value in dict.items():
        doc = process_actors(key,value)
        if not doc:
            dict[key] = ''
        else:
            dict[key] = ''.join(doc)
    return dict

def process_actors(key,value):
    #print('ACTOR:', value)

    doc = value.lower()
    #print('Convert to lowercase:', doc)

    doc = nlp(doc) 

    doc = clean_lemm(doc)
    #print('Lemmatization:', doc)

    doc = clean_dups(doc)       
    #print('Clean duplicates:', doc)

    doc = check_synset(doc)
    #print('Only words with Synsets:', doc)

    doc = check_lemma(doc)
    #print('Only words with Lemmas:', doc)

    doc = compare_actors(doc)
    #print('List after comparing actors descriptions:', doc)

    return doc

# lemmatization - remove stop words, ponctuation and numbers
def clean_lemm(doc):
    return [word.lemma_ for word in doc if (not word.is_stop and not word.is_punct and not word.like_num)]

# remove duplicates
def clean_dups(doc):
    res = []
    [res.append(x) for x in doc if x not in res]
    return res

# check if exists NOUN synset for descriptions - if not, remove from list
def check_synset(doc):
    return [word for word in doc if wn.synsets(word, pos=wn.NOUN)]

# check if exists NOUN lemma for descriptions - if not, remove from list
def check_lemma(doc):
    wn_lemmas = set(wn.all_lemma_names(pos='n'))
    return [word for word in doc if word in wn_lemmas]

# compare actor descriptions to get the most specific
def compare_actors(list):
    if len(list) == 1:
        return list
    else:
        l_hyps = []     # list of hypernyms
        l_spec = []     # list of most specific hypernyms
        final  = []     # final list after the tiebreaker

        # compare elements to get a list of hypernyms
        l_hyps = get_lowest_hyp(list)
        
        # compare elements from the list of hypernyms with the root to get the lowest common hypernyms
        # root = Synset('entity.n.01')
        root_name = 'entity'

        # check similarity between hypernyms in list of hyperyms to root (distance to the root)
        # the further from the root, the more specific
        control = 1
        for i in range(len(l_hyps)):
            sim = get_similarity(l_hyps[i],root_name)
            #print('Similarity(',l_hyps[i],',',root_name,'): ',sim)
            if sim < control:
                control = sim
                l_spec = [l_hyps[i]]        
            elif sim == control:
                control = sim
                l_spec.append(l_hyps[i])        
        #print('Most specif hypernyms: ',l_spec)  

        # tiebreaker for cases where hypernyms have the same distance to the root
        c = 10000
        for hyp in l_spec:
            count = len(get_synsets(hyp).hyponyms()) # how many hyponyms
            #print('Number of hyponyms for ',hyp,': ',count)
            if count < c:
                l_spec = [hyp] 
        #print('Most specif hypernym (after the tiebreaker): ',l_spec)

        # similarity between descriptions and the most specif hypernym to get the description 
        # with the highest score of similarity to the most specif hypernym, that is, the most specific.

        control = 0
        for i in range(len(list)):
            for j in range(len(l_spec)):
                sim = get_similarity(list[i],l_spec[j])
                #print('Similarity(',list[i],',',l_spec[j],'): ',sim)
                if sim > control:
                    control = sim
                    final = [list[i]]
        return final

# from list of synsets of word, get the first synset that is NOUN
def get_synsets(word):
    return wn.synset(word + '.n.01')

# score of how similar two word senses are, in the range 0 to 1
def get_similarity(word1,word2):
    return get_synsets(word1).path_similarity(get_synsets(word2))
    
# from list terms, get list with lowest commom hypernyms
def get_lowest_hyp(list):
    l = []
    for i in range(len(list)):
        for j in range(i+1,len(list)):
            l.append(get_hypernym(list[i],list[j]))
    #print('List of hypernyms: ', l)
    l_hyps = clean_dups(l)
    #print('List of hypernyms (no dups): ', l_hyps)
    return l_hyps

# get hypernym between two elements
def get_hypernym(x,y):
    hyp = wn.synset(x + '.n.01').lowest_common_hypernyms(wn.synset(y + '.n.01'))
    hyp_name = wn.synset(hyp[0].name()).lemma_names()[0]
    #print('Hypernym(',x,',',y,'): ', hyp_name)
    return hyp_name