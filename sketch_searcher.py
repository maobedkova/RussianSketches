# coding: utf-8

__author__ = "maobedkova"

import fnmatch
import os
import pickle
import sys
from sketch_generator import SketchEntry

def get_sketches_by_word(word, path, ex_number):
    """The function for getting sketches for a given word"""
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, word + '.pkl'):
            print ('FILENAME', filename)
            with open(path + filename, 'rb') as sk:
                sketch = pickle.load(sk)
                for linkage in sketch:
                    print ('LINKAGE', linkage)
                    for obj in sorted(sketch[linkage], reverse=True)[:int(ex_number)]:
                        print (obj.first_word,
                               obj.first_word_pos,
                               obj.second_word,
                               obj.second_word_pos,
                               obj.third_word,
                               obj.third_word_pos,
                               obj.linkage,
                               obj.abs_freq,
                               round(obj.dice, 3),
                               round(obj.chi, 3),
                               round(obj.t_score, 3),
                               round(obj.poisson_stirling, 3),
                               round(obj.pmi, 3),
                               round(obj.mi, 3),
                               round(obj.likelihood_ratio, 3),
                               round(obj.jaccard, 3),
                               round(obj.fisher, 3))


if __name__ == '__main__':
    try:
        word = sys.argv[1]
        path = sys.argv[2]
        ex_number = sys.argv[3]
    except:
        word = input('Enter a word: ')
        path = input('Enter a path to sketch files: ')
        ex_number = input('Enter a number of examples: ')
    get_sketches_by_word(word, path, ex_number)