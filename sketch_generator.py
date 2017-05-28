# coding: utf-8

__author__ = "maobedkova"

import os
import pickle
import pymorphy2
import sys
from association_measures import count_statistics

morph = pymorphy2.MorphAnalyzer()

class RussianSketches:
    """The class of Russian sketches which contains sketches for words"""

    def __init__(self, input_file, noun, adj, verb, adv, adp, praed, punct, adp_mark=False):
        """Attrbutes of the RussianSketches class"""
        self.input_file = input_file
        self.candidates = {}            # dictionary of sketch entries grouped by words and linkages
        self.filtered_candidates = {}   # dictionary of filtered by a part of speech sketch candidates
        self.bigram_corpus_size = 0     # number of bigrams in a corpus
        self.trigram_corpus_size = 0    # number of trigrams in a corpus
        self.adp_mark = adp_mark        # if False noun is dependent of adposition; if True adposition is dependent of noun
        self.adp = adp                  # tag for adposition
        self.punct = punct              # tag for punctuation marks
        self.possible_bigrams = {
            noun: [adj, adv, verb, noun],
            adj: [adv, noun],
            verb: [adv, noun],
            adv: [verb, noun],
            praed: [adv, noun, verb]
        }                               # dictionary of part of speeches that are allowed for bigrams
        self.possible_trigrams = {
            noun: {adp: [noun, verb]},
            adj: {adp: [noun]},
            verb: {adp: [noun]},
            praed: {adp: [noun]}
        }                               # dictionary of part of speeches that are allowed for trigrams
        self.pymorphy_dict = {'ADJF': adj,
                              'ADJS': adj,
                              'PRED': praed,
                              'ADVB': adv,
                              'VERB': verb,
                              'NOUN': noun}    # dictionary of pymorphy tags and their equivalents

    def lemmatization(self, word, pos, morph=morph):
        """The function for word lemmatization"""
        for i in range(0, len(morph.parse(word))):
            p = morph.parse(word)[i]
            if p.tag.POS in self.pymorphy_dict and self.pymorphy_dict[p.tag.POS] == pos:
                lemma = p.normal_form
            else:
                lemma = morph.parse(word)[0].normal_form
        return lemma

    def reading_conll(self):
        """The function for reading conll files"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            infos = []
            i = 0
            for line in f:
                if line.startswith('#'):
                    continue
                if i % 10000 == 0:
                    print (i, flush=True)
                if len(line) == 1:
                    yield infos
                    infos = []
                    continue
                splitted = line.strip().split('\t')
                if splitted[2] == '_':
                    lemma = self.lemmatization(splitted[1], splitted[3])
                else:
                    lemma = splitted[2]
                infos.append([splitted[0],  # number of a wordform
                              lemma,        # lemma
                              splitted[3],  # part of speech
                              splitted[6],  # head word
                              splitted[7]]) # type of a linkage
                i += 1

    def add_sketch_entry(self, linkage,
                         first_word, first_word_pos,
                         second_word, second_word_pos,
                         third_word=None, third_word_pos=None):
        """The function for adding new sketch candidates in a dictionary"""

        def create_entry(key, linkage=linkage,
                         first_word=first_word, first_word_pos=first_word_pos,
                         second_word=second_word, second_word_pos=second_word_pos,
                         third_word=third_word, third_word_pos=third_word_pos):
            """The function for creating a new sketch entry"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos, linkage,
                             third_word, third_word_pos)
            sl.abs_freq = 1
            self.candidates[key] = {linkage: [sl]}

        def add_entry(key, linkage=linkage,
                      first_word=first_word, first_word_pos=first_word_pos,
                      second_word=second_word, second_word_pos=second_word_pos,
                      third_word=third_word, third_word_pos=third_word_pos):
            """The function for adding a new sketch entry to an existing linkage"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos, linkage,
                             third_word, third_word_pos)
            sl.abs_freq = 1
            self.candidates[key][linkage] += [sl]

        def add_linkage(key, linkage=linkage,
                        first_word=first_word, first_word_pos=first_word_pos,
                        second_word=second_word, second_word_pos=second_word_pos,
                        third_word=third_word, third_word_pos=third_word_pos):
            """The function for adding a new linkage in a bigram sketch entry"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos, linkage,
                             third_word, third_word_pos)
            sl.abs_freq = 1
            self.candidates[key][linkage] = [sl]

        def change_entry(info, word, linkage=linkage,
                         first_word=first_word, first_word_pos=first_word_pos,
                         second_word=second_word, second_word_pos=second_word_pos,
                         third_word=third_word, third_word_pos=third_word_pos):
            """The function for changing a sketch entry"""
            for obj in info:
                if first_word == obj.first_word and first_word_pos == obj.first_word_pos and \
                                second_word == obj.second_word and second_word_pos == obj.second_word_pos and \
                                third_word == obj.third_word and third_word_pos == obj.third_word_pos:
                    for obj in self.candidates[word][linkage]:
                        if first_word == obj.first_word and first_word_pos == obj.first_word_pos and \
                                        second_word == obj.second_word and second_word_pos == obj.second_word_pos and \
                                        third_word == obj.third_word and third_word_pos == obj.third_word_pos:
                            obj.abs_freq += 1
                            return True

        def check_linkages_and_entries(word, tmp_dict, linkage=linkage):
            """The function for checking if linkage or entry exists"""
            if word in tmp_dict:
                if linkage in tmp_dict[word]:
                    if not change_entry(tmp_dict[word][linkage], word):
                        add_entry(word)
                else:
                    add_linkage(word)

        def deepcopy(dictionary):
            new_dictionary = {}
            for item in dictionary:
                new_dictionary[item] = dictionary[item]
            return new_dictionary

        # Check if it is the first entry
        if not self.candidates:
            create_entry(first_word)
            create_entry(second_word)
            if third_word:
                create_entry(third_word)
        # Changing existing sketch entries
        else:
            tmp_dict = deepcopy(self.candidates)
            check_linkages_and_entries(first_word, tmp_dict)
            check_linkages_and_entries(second_word, tmp_dict)
            check_linkages_and_entries(third_word, tmp_dict)
            if first_word not in tmp_dict:
                create_entry(first_word)
            if second_word not in tmp_dict:
                create_entry(second_word)
            if third_word:
                if third_word not in tmp_dict:
                    create_entry(third_word)

    def retrieve_candidates(self):
        """The function for retrieving candidates for sketches"""

        def add_trigram(head, bigram_allowed):
            """The function for adding trigrams"""
            if head[2] == self.adp or head[1].lower() == 'и':
                self.trigram_corpus_size += 1
                self.add_sketch_entry(
                    info_1[2] + '_' + info_2[2] + '_' + info_3[2],  # type of a linkage
                    info_1[1],                                      # first word
                    info_1[2],                                      # part of speech of a first word
                    info_2[1],                                      # second word
                    info_2[2],                                      # part of speech of a second word
                    info_3[1],                                      # third word
                    info_3[2]                                       # part of speech of a third word
                )
                bigram_allowed = False
            return bigram_allowed

        print ('=== Retrieving candidates ===', flush=True)
        for infos in self.reading_conll():
            for info_1 in infos:
                if info_1[2] == self.punct:
                    continue
                for info_2 in infos:
                    if info_2[2] == self.punct:
                        continue
                    bigram_allowed = True
                    # Retrieving trigram candidates
                    for info_3 in infos:
                        if info_3[2] == self.punct:
                            continue
                        if info_1[0] == info_2[3] and info_2[0] == info_3[3]:
                            if self.adp_mark:
                                bigram_allowed = add_trigram(info_3, bigram_allowed)
                            else:
                                bigram_allowed = add_trigram(info_2, bigram_allowed)
                    # Retrieving bigram candidates
                    if bigram_allowed:
                        if info_1[0] == info_2[3]:
                            self.bigram_corpus_size += 1
                            self.add_sketch_entry(
                                info_2[4],  # type of a linkage
                                info_1[1],  # first word
                                info_1[2],  # part of speech of a first word
                                info_2[1],  # second word
                                info_2[2]   # part of speech of a second word
                            )

    def filtering(self):
        """The function for filtering linkages for every part of speech"""
        print ('=== Filtering candidates ===', flush=True)

        def create_candidates_dict(dict, word, linkage, arr):
            """The function for creating any dictionaries with sketch entries grouped by words and linkages"""
            if word in dict:
                if linkage in dict[word]:
                    dict[word][linkage] += arr  # add candidates
                else:
                    dict[word][linkage] = arr  # add linkage + candidates
            else:
                dict[word] = {linkage: arr}  # add word + linkage + candidates

        def filter_check_trigrams(word, pos1, pos2, pos3, obj, linkage):
            """The function for checking the presence in the dictionary"""
            if pos1 in self.possible_trigrams \
                    and pos2 in self.possible_trigrams[pos1] \
                    and pos3 in self.possible_trigrams[pos1][pos2]:
                create_candidates_dict(self.filtered_candidates, word, linkage, [obj])
                return True

        def filter_check_conj(word, word2, pos2, pos3, obj, linkage):
            """The function for checking the presence of the conjunction и"""
            if word.lower() == 'и' and pos2 == pos3:
                create_candidates_dict(self.filtered_candidates, word2, linkage, [obj])
                return True

        def filter_pos(word, obj, linkage):
            """The function for filtering linkages by a given part of speech"""
            # Filtering trigrams
            if obj.third_word:
                if word == obj.first_word:
                    if not filter_check_conj(obj.second_word, obj.first_word,
                                             obj.first_word_pos, obj.third_word_pos, obj, linkage):
                        if not filter_check_conj(obj.third_word, obj.first_word,
                                                 obj.first_word_pos, obj.second_word_pos, obj, linkage):
                            if not filter_check_trigrams(word, obj.first_word_pos, obj.second_word_pos,
                                                         obj.third_word_pos, obj, linkage):
                                filter_check_trigrams(word, obj.first_word_pos, obj.third_word_pos,
                                                      obj.second_word_pos, obj, linkage)
                elif word == obj.second_word:
                    if not filter_check_conj(obj.first_word, obj.second_word,
                                             obj.second_word_pos, obj.third_word_pos, obj, linkage):
                        if not filter_check_conj(obj.third_word, obj.second_word,
                                                 obj.first_word_pos, obj.second_word_pos, obj, linkage):
                            if not filter_check_trigrams(word, obj.second_word_pos, obj.first_word_pos,
                                                         obj.third_word_pos, obj, linkage):
                                filter_check_trigrams(word, obj.second_word_pos, obj.third_word_pos,
                                                      obj.first_word_pos, obj, linkage)
                else:
                    if not filter_check_conj(obj.second_word, obj.third_word,
                                             obj.first_word_pos, obj.third_word_pos, obj, linkage):
                        if not filter_check_conj(obj.first_word, obj.third_word,
                                                 obj.third_word_pos, obj.second_word_pos, obj, linkage):
                            if not filter_check_trigrams(word, obj.third_word_pos, obj.second_word_pos,
                                                         obj.first_word_pos, obj, linkage):
                                filter_check_trigrams(word, obj.third_word_pos, obj.first_word_pos,
                                                      obj.second_word_pos, obj, linkage)
            # Filtering bigrams
            else:
                if word == obj.first_word:
                    if obj.first_word_pos in self.possible_bigrams \
                            and obj.second_word_pos in self.possible_bigrams[obj.first_word_pos]:
                        create_candidates_dict(self.filtered_candidates, word, linkage, [obj])
                else:
                    if obj.second_word_pos in self.possible_bigrams \
                            and obj.first_word_pos in self.possible_bigrams[obj.second_word_pos]:
                        create_candidates_dict(self.filtered_candidates, word, linkage, [obj])

        for word in self.candidates:
            for linkage in self.candidates[word]:
                for obj in self.candidates[word][linkage]:
                    filter_pos(word, obj, linkage)

    def count_association_measures(self):
        """The function for counting a chosen association measure"""
        count_statistics(self.candidates, self.bigram_corpus_size, self.trigram_corpus_size)

    def show_results(self):
        """The function for showing the results"""

        def print_sketches(arr):
            """The function for printing out sketches"""
            print (arr)
            for word in arr:
                print ('WORD', word)
                for link in arr[word]:
                    print ('LINKAGE', link)
                    for obj in arr[word][link]:
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
                print ('='*30)

        print ('=== Results ===')
        if self.filtered_candidates:
            print_sketches(self.filtered_candidates)
        else:
            print_sketches(self.candidates)

    def writing_down_results(self):
        """The function for writing down the results in .json"""
        print ('=== Writing down the results ===', flush=True)

        def create_files(arr):
            """The function for creating sketch files in a sketch directory"""
            for word in arr:
                sketches = open('sketches/' + word + '.pkl', 'wb')
                pickle.dump(arr[word], sketches, pickle.HIGHEST_PROTOCOL)
                sketches.close()

        if not os.path.exists('sketches'):
            os.mkdir('sketches')
        if self.filtered_candidates:
            create_files(self.filtered_candidates)
        else:
            create_files(self.candidates)


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


# The main function which calling the RussianSketches class
if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
    except:
        input_file = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/sketch_test_2.conll'
    rs = RussianSketches(input_file, 'S', 'A', 'V', 'ADV', 'PR', None, 'PUNC') # RuSyntax, SynTagRus
    # rs = RussianSketches(input_file, 'NOUN', 'ADJ', 'VERB', 'ADV', 'ADP', None, 'PUNCT', True) # SyntaxNet
    rs.retrieve_candidates()
    rs.count_association_measures()
    rs.filtering()
    rs.show_results()
    rs.writing_down_results()