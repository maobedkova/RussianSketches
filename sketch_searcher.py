# coding: utf-8

__author__ = "maobedkova"

import fnmatch
import os
import pickle
import sys
from sketch_generator import SketchEntry

def get_sketches_by_word(word):
    """The function for getting sketches for a given word"""
    for filename in os.listdir('sketches'):
        if fnmatch.fnmatch(filename, word + '.pkl'):
            print ('FILENAME', filename)
            with open('sketches/' + filename, 'rb') as sk:
                sketch = pickle.load(sk)
                # Ranging sketches for a word
                for linkage in sketch:
                    print ('LINKAGE', linkage)
                    for obj in sorted(sketch[linkage], reverse=True)[:10]:
                        print (obj.first_word,
                               obj.first_word_pos,
                               obj.second_word,
                               obj.second_word_pos,
                               obj.third_word,
                               obj.third_word_pos,
                               obj.linkage,
                               obj.abs_freq,
                               obj.dice,
                               obj.chi,
                               obj.t_score,
                               obj.poisson_stirling,
                               obj.pmi,
                               obj.mi,
                               obj.likelihood_ratio,
                               obj.jaccard,
                               obj.fisher)


if __name__ == '__main__':
    try:
        word = sys.argv[1]
    except:
        word = input('Enter a word: ')
    get_sketches_by_word(word)