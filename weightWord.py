import copy
from pprint import pprint

def weight_word(sentence: str, get_total_weight=True):
    alphabet = 'оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё'
    l = [i for i in alphabet]
    weight = 0
    dictwords = {}
    sentence = sentence.strip().split(' ')
    memory = ''
    for word in sentence:
        for letter in word.lower():
            for letter_compare in l: 
                if letter == letter_compare:
                    weight += l.index(letter) + 1  

        dictwords[word] = f'{weight} ед.'
        weight = 0
                

    sorted_dict = {}
    sorted_keys = sorted(dictwords, key=dictwords.get, reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = dictwords[w]
    
    # if get_total_weight == True:
    #     return sorted_dict, sum([sorted_dict[i] for i in sorted_dict])
    # return sorted_dict

    return str(sorted_dict)

# print(weight_word(str(input('Sentence: '))))

