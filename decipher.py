import json
from numpy import argmax
from typing import List

def decipher_phrase(phrase:str, lexicon_filename:str, abc_filename:str):
    """
    Deciphering a phrase of words by lexicon

    :param phrase: The Ciphered phrase
    :param lexicon_filename: The lexicon file path
    :param abc_filename: The abc file path
    :return: De-Ciphered string
    """

    print(f'starting deciphering using {lexicon_filename} and {abc_filename}')
    abc = create_abc_list(abc_filename)
    lexicon = create_lexicon_list(lexicon_filename)

    phrase_words = phrase.split() # Split string into list of words by default using seperator ' '
    phrase_map = {}
    for word in phrase_words:
        phrase_map[word] = []
        length_of_chars = len(word)
        for lex_word in lexicon :
            temp_lex_word = lex_word.split()[0]
            if length_of_chars == len(temp_lex_word) :
                phrase_map[word].append(temp_lex_word) #List of optional worlds

    min_value = float('INF')
    min_options_word = None

    for k in phrase_map:
        if len(phrase_map[k]) < min_value:
            min_value = len(phrase_map[k])
            min_options_word = k

    good_k = find_good_k(phrase_map,min_options_word,abc)
    undeciper_phrase = undeciper(phrase, good_k, abc)
    #print(len(optional_word_list))
    result = {"orig_phrase": undeciper_phrase, "K": good_k}
    return result

###########################################HELP_FUNCTIONS##############################################

#open file and return abc letters list
def create_abc_list (abc_filename:str):
    with open(abc_filename,'r',encoding='utf8') as f:
        abc = []
        temp_abc = f.readlines()
        for char in temp_abc:
          abc.append(char.strip())
        f.close()
    return abc

#open file of lexcicon and return lexcicon words list
def create_lexicon_list (lexicon_filename:str):
    with open(lexicon_filename, 'r', encoding='utf8') as f:
        lexicon = f.readlines()
        f.close()
    return lexicon

def find_good_k(phrase_map,min_options_word,abc) :
    """

    :param phrase_map: gets the dictonery which contain the match lists for each cripted word
    :param min_options_word: the index of the list with minimum words to check
    :param abc:
    :return: the good k to chiper phrase
    """
    for optional_word in phrase_map[min_options_word] :
        for i in range(0, 25):
            if check_word_cipher(min_options_word,optional_word,i,abc):
                print(f'Found k : {i}')
                return i
            else:
                print(f'Not found k ! continuing.')

def convert_char_cipher(optional_char:str, tested_k:int, abc:List[str]) -> str:
    """
    Convert a char into the ciphered version

    :param optional_char: gets the checked char
    :param tested_k: gets the tested k
    :param abc: gets list of abc letters
    :return: the converted letter
    """
    current_index = abc.index(optional_char) + tested_k
    if current_index >=25:
        delta = current_index - 25
        corrected_index = delta
    else :
        corrected_index = abc.index(optional_char) + tested_k

    target_char = abc[corrected_index]

    return target_char

def check_word_cipher(ciphered_word,optional_word,k,abc):
    """
    Check a word by optional k

    :param ciphered_word: gets the ciphered word
    :param optional_word: gets the optional word that matches the cripted word before cipher
    :param k: the tested k- number
    :param abc: a list of alpha bet
    :return: bool
    """

    char_index = 0
    chars_tests = []
    for char in optional_word:
        decipher_test_char = convert_char_cipher(char, k, abc)
        is_decipherd = ciphered_word[char_index] == decipher_test_char
        if is_decipherd:
            chars_tests.append(is_decipherd)
        char_index+=1
    if len(chars_tests) == len(ciphered_word):
        return True
    else:
        return False

def undeciper(phrase, good_k, abc) :
    """
    :param phrase: gets the cipher phrase
    :param good_k: gets the correct k to solve the incripted phrase
    :param abc: list of abc letters
    :return: the dechiper phrase
    """
    phrase_list = phrase.split()
    new_phrase_list = []

    for word in phrase_list :
        letters_list = list(word)
        new_letters_list = []

        for letter in letters_list :
            new_letter = convert_char_cipher(letter, 25-good_k, abc)
            new_letters_list.append(new_letter)

        new_word = "".join(new_letters_list)
        new_phrase_list.append(new_word)

    undicper_phrase = " ".join(new_phrase_list)
    return undicper_phrase

if __name__ == '__main__':
    with open('config-decipher.json', 'r') as json_file:
        config = json.load(json_file)

    result = decipher_phrase(config['secret_phrase'],
                             config['lexicon_filename'],
                             config['abc_filename'])

    if result:
        print(f'deciphered phrase: {result["orig_phrase"]}, K: {result["K"]}')
    else:
        print("Cannot decipher the phrase!")
