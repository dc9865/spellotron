"""
file: spellotron.py
author: Daniel Cho
purpose: mainly deals with the cases when the program's
running modes(words, lines only, and lines with text
files) are different and print different messages and
words for each case.
"""
import sys
from spell_check import *

def main():
    """
    deals with the cases for words and lines modes
    """
    if len(sys.argv) < 2:
        print("Houston, we have a problem.", file = sys.stderr)
        exit()
    #when the words mode comes in
    if sys.argv[1] == 'words':
        line = sys.stdin.readline()
        words = line.split()
        corrected_lst, unknown_lst = readfile(words, sys.argv[1])
        print("\n", len(words), "words read from file.")
        print("\n", len(corrected_lst), "Corrected Words")
        print(corrected_lst)
        print("\n", len(unknown_lst), "Unknown Words")
        print(unknown_lst)
    #when the lines mode comes in
    elif sys.argv[1] == 'lines':
        #when only one line comes in
        if len(sys.argv) == 2:
            line = sys.stdin.readline()
            words = line.split()
            corrected_lst, unknown_lst = readfile(words, sys.argv[1])
            print("\n", len(words), "words read from file.")
            print("\n", len(corrected_lst), "Corrected Words")
            print(corrected_lst)
            print("\n", len(unknown_lst), "Unknown Words")
            print(unknown_lst)
        else:   #when lines with text files come in
            word_num = 0
            total_corrected_lst = []
            total_unknown_lst = []
            try:
                text_source = open(sys.argv[2])
                for line in text_source:
                    words = line.split()
                    word_num += len(words)
                    corrected_lst, unknown_lst = readfile(words, "file")
                    total_corrected_lst += corrected_lst
                    total_unknown_lst += unknown_lst

                print("\n", word_num, "words read from file.")
                print("\n", len(total_corrected_lst), "Corrected Words")
                total_corrected_lst.sort()
                print(total_corrected_lst)
                print("\n", len(total_unknown_lst), "Unknown Words")
                total_unknown_lst.sort()
                print(total_unknown_lst)

            except IOError:
                print("Houston, we have a problem.", file=sys.stderr)

            if text_source != sys.stdin:
                text_source.close()

main()

