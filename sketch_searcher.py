# coding: utf-8

__author__ = "maobedkova"

import fnmatch
import os
import pickle
import sys


class SketchEntry:
    """The class of sketch entry which creates entries for sketches used in Russian sketches class"""

    def __init__(self, first_word, first_word_pos,
                 second_word, second_word_pos, linkage,
                 third_word=None, third_word_pos=None):
        """Attrbutes of the SketchEntry class"""
        self.first_word = first_word            # first word text
        self.first_word_pos = first_word_pos    # part of speech of a first word
        self.second_word = second_word          # second word text
        self.second_word_pos = second_word_pos  # part of speech of a second word
        self.third_word = third_word            # third word text
        self.third_word_pos = third_word_pos    # part of speech of a third word
        self.linkage = linkage                  # type of a linkage
        self.abs_freq = 0                       # absolute frequency of the first word - second word collocation
        # Different association measures for sketches
        self.dice = 0               # + +
        self.poisson_stirling = 0   # + +
        self.fisher = 0             # +
        self.chi = 0                # + +
        self.likelihood_ratio = 0   # + +
        self.mi = 0                 # + +
        self.jaccard = 0            # + +
        self.pmi = 0                # + +
        self.t_score = 0            # + +

    # Rewriting ==, !=, <, >, <=, >= python functions for proper sorting of sketches
    def __eq__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling == other.poisson_stirling
        elif metric == 'chi':
            return self.chi == other.chi
        elif metric == 'pmi':
            return self.pmi == other.pmi
        elif metric == 'mi':
            return self.mi == other.mi
        elif metric == 'jaccard':
            return self.jaccard == other.jaccard
        elif metric == 't-score':
            return self.t_score == other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio == other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher == other.fisher
        else:
            return self.dice == other.dice

    def __ne__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling != other.poisson_stirling
        elif metric == 'chi':
            return self.chi != other.chi
        elif metric == 'pmi':
            return self.pmi != other.pmi
        elif metric == 'mi':
            return self.mi != other.mi
        elif metric == 'jaccard':
            return self.jaccard != other.jaccard
        elif metric == 't-score':
            return self.t_score != other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio != other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher != other.fisher
        else:
            return self.dice != other.dice

    def __lt__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling < other.poisson_stirling
        elif metric == 'chi':
            return self.chi < other.chi
        elif metric == 'pmi':
            return self.pmi < other.pmi
        elif metric == 'mi':
            return self.mi < other.mi
        elif metric == 'jaccard':
            return self.jaccard < other.jaccard
        elif metric == 't-score':
            return self.t_score < other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio < other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher < other.fisher
        else:
            return self.dice < other.dice

    def __gt__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling > other.poisson_stirling
        elif metric == 'chi':
            return self.chi > other.chi
        elif metric == 'pmi':
            return self.pmi > other.pmi
        elif metric == 'mi':
            return self.mi > other.mi
        elif metric == 'jaccard':
            return self.jaccard > other.jaccard
        elif metric == 't-score':
            return self.t_score > other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio > other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher > other.fisher
        else:
            return self.dice > other.dice

    def __le__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling <= other.poisson_stirling
        elif metric == 'chi':
            return self.chi <= other.chi
        elif metric == 'pmi':
            return self.pmi <= other.pmi
        elif metric == 'mi':
            return self.mi <= other.mi
        elif metric == 'jaccard':
            return self.jaccard <= other.jaccard
        elif metric == 't-score':
            return self.t_score <= other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio <= other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher <= other.fisher
        else:
            return self.dice <= other.dice

    def __ge__(self, other):
        if metric == 'poisson-stirling':
            return self.poisson_stirling >= other.poisson_stirling
        elif metric == 'chi':
            return self.chi >= other.chi
        elif metric == 'pmi':
            return self.pmi >= other.pmi
        elif metric == 'mi':
            return self.mi >= other.mi
        elif metric == 'jaccard':
            return self.jaccard >= other.jaccard
        elif metric == 't-score':
            return self.t_score >= other.t_score
        elif metric == 'likelihood-ratio':
            return self.likelihood_ratio >= other.likelihood_ratio
        elif metric == 'fisher':
            return self.fisher >= other.fisher
        else:
            return self.dice >= other.dice


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
                        if obj.abs_freq < 3:
                            continue
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
        metric = sys.argv[3]
        ex_number = sys.argv[4]
    except:
        word = input('Enter a word: ')
        path = input('Enter a path to sketch files: ')
        metric = input('Enter a metric for ranging: ')
        ex_number = input('Enter a number of examples: ')
    get_sketches_by_word(word, path, ex_number)