"""
file: spell_check.py
author: Daniel Cho
purpose: checks the spellings of each letter of words
or lines that you manually type in or that are to read
from text files and corrects words that were wrong
spelled by any means such as typing an adjacent key or
extra key or deleting a key.
"""

LEGAL_WORD_FILE = "american-english.txt"
KEY_ADJACENCY_FILE = "keyboard-letters.txt"
ALPHABET = tuple(chr(code) for code in range(ord('a'), ord('z') + 1))
ENGLISH_DICT = {}

def make_english_dict():
    """
    Reads LEGAL_WORD_FILE line
    by line for each word stored in the
    file and to compare legal words, store
    the key words in ENGLISH_DICT.
    """

    f = open(LEGAL_WORD_FILE, encoding="utf-8")
    for line in f:
        word = line.split()
        word = word[0]
        ENGLISH_DICT[word] = None
    f.close()

def readfile(input_lst, mode):
    """

    :param input_lst: a group of words that are splitted in a list form
    :param mode: one of the program's running mode(words, lines or lines with text files)
    :return: corrected_lst: lists of corrected words
    unknown_lst: lists of words that cannot be corrected.
    """
    misspell_lst = []
    corrected_lst = []
    unknown_lst = []

    make_english_dict()
    result_lst = input_lst

    #check to see if the words are legal words and
    #store those words that are not legal words in misspell_lst.
    for word in input_lst:
        word = word.strip(",.\"\';:-!?_[]{}()@#ˆ&*+=/").lower()
        if word not in ENGLISH_DICT:
            misspell_lst.append(word)

    for k in misspell_lst:
        possible_lst = []
        if adj_edit(k) != []:
            corrected_lst.append(k)
            possible_lst = adj_edit(k)
        elif insert_edit(k) != []:
            corrected_lst.append(k)
            possible_lst = insert_edit(k)
        elif deletes(k) != []:
            corrected_lst.append(k)
            possible_lst = deletes(k)
        else:
            unknown_lst.append(k)

        if possible_lst != []:
            corrected_word = correction(possible_lst)
            if mode == "words":
                print(k, '->', corrected_word)
            elif mode == "lines" or mode == "file":
                result_lst = [w.replace(k, corrected_word) for w in result_lst]

    if mode == "lines" or mode == "file":
        print(" ".join(result_lst))
    return corrected_lst, unknown_lst

def correction(possible_lst):
    """
    pick only one of the possible spelling corrected word.
    :param possible_lst: corrected words in a list form
    :return: one that comes first from the possible spelling corrected words
    """
    for i in possible_lst:
        if i in ENGLISH_DICT:
            corrected_word = i
            break
    return corrected_word


def known(words):
    """
    returns the subset of words that appear in the dictionary of words
    """
    return (list(set(w for w in words if w in ENGLISH_DICT)))

def edit_splits(word):
    """
    split words from right to left.
    :param word: words that are incorrect and need to be corrected
    :return: the splited words in a list form.
    """
    splits = []
    for i in range(len(word) + 1):
        splits += [(word[:i], word[i:])]
    return splits

def adj_edit(word):
    """
    edits the letters of the words with adjacent letters.
    :param word: words that are incorrect and need to be corrected
    :return: the edited words in a list form
    """
    adj_replaces = []
    splits = edit_splits(word)
    f = open(KEY_ADJACENCY_FILE, encoding="utf-8")
    for line in f:
        adj_letters = line.split()
        for L, R in splits:
            if R:
                for c in adj_letters:
                    if R[0] == adj_letters[0]:
                        adj_replaces += [L + c + R[1:]]
    f.close()
    return known(adj_replaces)

def insert_edit(word):
    """
    inserts a letter to the words
    :param word: words that are incorrect and need to be corrected
    :return: words that have an inserted letter in a list form
    """
    inserts = []
    splits = edit_splits(word)

    for L, R in splits:
        for c in ALPHABET:
            inserts += [L + c + R ]
    return known(inserts)

def deletes(word):
    """
    deletes a letter in the words
    :param word: words that are incorrect and need to be corrected
    :return: words that have a deleted letter in a list form
    """
    deletes = []
    splits = edit_splits(word)

    for L, R in splits:
        if R:
            deletes += [L + R[1:]]
    return known(deletes)
