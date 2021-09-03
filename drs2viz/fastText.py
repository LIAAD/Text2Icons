#-----------------------------------------------
#                   fastText
#-----------------------------------------------
# 'wiki-news-300d-1M-subword.bin' -> https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.bin.zip

from scipy.spatial import distance
import fasttext

model = fasttext.load_model('./wiki-news-300d-1M-subword.bin')

def replaceUnder(word):
    return word.replace("_", " ")

def getVec(word):
    return model.get_word_vector(word)

def calcCosineSimilarity(word1,word2):
    result = 1 - distance.cosine(getVec(word1), getVec(word2))
    return result

def getMostSimilar(term,list):
    mostSimilarValue = 0
    mostSimilarTerm = ''
    for item in list:
        item_n = replaceUnder(item)
        c = calcCosineSimilarity(term,item_n)
        if c > mostSimilarValue:
            mostSimilarValue = c
            mostSimilarTerm = item
    return mostSimilarTerm

def getLeastSimilar(term,list):
    leastSimilarValue = 1
    leastSimilarTerm = ''
    for item in list:
        item_n = replaceUnder(item)
        c = calcCosineSimilarity(term,item_n)
        if c < leastSimilarValue:
            leastSimilarValue = c
            leastSimilarTerm = item
    return leastSimilarTerm

def get2MostSimilar(term,list):
    if len(list) == 1:                  # if there is only one element in the list
        sMostSimilarTerm = list[0]
    
    else:
        c_list = []

        for item in list:
            item_n = replaceUnder(item)
            c = calcCosineSimilarity(term,item_n)
            c_list.append(c)

        original = c_list

        s_list = sorted(c_list)                     # similarities list sorted
        sMostSimilarValue = s_list[-2]              # second largest similarity
        index = original.index(sMostSimilarValue)   # index of second largest similarity
        sMostSimilarTerm = list[index]              # second most similar word

    return sMostSimilarTerm