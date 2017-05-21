# # Ranging candidates and saving the ranged candidates as an attribute
# print ('=== Ranging candidates ===')
# for ranged_candidates, linkage, word in ranging(self.candidates):
#     self.create_candidates_dict(self.ranged_candidates, word, linkage, ranged_candidates)\

import fnmatch
import os
import pickle
import sys
from sketch_generator import SketchEntry

def get_sketches_by_word(word):
    for filename in os.listdir('sketches'):
        if fnmatch.fnmatch(filename, word + '.pkl'):
            print ('FILENAME', filename)
            with open('sketches/' + filename, 'rb') as sk:
                sketch = pickle.load(sk)
                for link in sketch:
                    print ('LINKAGE', link)
                    for obj in sketch[link]:
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