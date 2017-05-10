import copy
from association_measures import get_contingency_table, ranging

path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'sketch_test.conll'

class RussianSketches:
    """The class of Russian sketches which contains sketches for words"""

    def __init__(self):
        """Attrbutes of the RussianSketches class"""
        self.candidates = {}            # dictionary of sketch entries grouped by words and linkages
        self.ranged_candidates = {}     # dictionary of ranged by a statistics sketch candidates
        self.filtered_candidates = {}   # dictionary of filtered by a part of speech sketch candidates
        self.corpus_size = 0            # number of bigrams in a corpus

    def reading_conll(self):
        """The function for reading conll files"""
        with open(path + input_file, 'r', encoding='utf-8') as f:
            infos = []
            for line in f:
                if len(line) == 1:
                    yield infos
                    infos = []
                    continue
                splitted = line.strip().split('\t')
                infos.append([splitted[0],  # number of a wordform
                              splitted[1],  # wordform
                              splitted[3],  # part of speech
                              splitted[6],  # head word
                              splitted[7]]) # type of a linkage

    def add_new_sketch_entry(self, first_word, first_word_pos, second_word, second_word_pos, linkage):
        """The function for adding new sketch candidates in a dictionary"""

        def create_sketch_entry(first_word, first_word_pos,
                                second_word, second_word_pos,
                                head, linkage=linkage):
            """The function for creating a new sketch entry"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos,
                             linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word] = {linkage: [sl]}

        def add_sketch_entry(first_word, first_word_pos,
                             second_word, second_word_pos,
                             head, linkage=linkage):
            """The function for adding a new sketch entry"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos,
                             linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word][linkage] += [sl]

        def add_new_linkage(first_word, first_word_pos,
                            second_word, second_word_pos,
                            head, linkage=linkage):
            """The function for adding a new linkage"""
            sl = SketchEntry(first_word, first_word_pos,
                             second_word, second_word_pos,
                             linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word][linkage] = [sl]

        def change_sketch_entry(info, first_word, first_word_pos,
                                second_word, second_word_pos,
                                head, linkage=linkage):
            """The function for changing a sketch entry"""
            for obj in info:
                if first_word == obj.first_word and first_word_pos == obj.first_word_pos and \
                        second_word == obj.second_word and second_word_pos == obj.second_word_pos and \
                                linkage == obj.linkage and obj.head == head:
                    obj.abs_freq += 1
                    return True

        # Check if it is the first entry
        if not self.candidates:
            create_sketch_entry(first_word, first_word_pos,
                                second_word, second_word_pos, 1)
            create_sketch_entry(second_word, second_word_pos,
                                first_word, first_word_pos, 2)
        # Changing existing sketch entries
        else:
            tmp_dict = copy.deepcopy(self.candidates)
            if first_word in tmp_dict:
                if linkage in tmp_dict[first_word]:
                    if not change_sketch_entry(tmp_dict[first_word][linkage],
                                               first_word, first_word_pos,
                                               second_word, second_word_pos, 1):
                        add_sketch_entry(first_word, first_word_pos,
                                         second_word, second_word_pos, 1)
                else:
                    add_new_linkage(first_word, first_word_pos,
                                    second_word, second_word_pos, 1)
            if second_word in tmp_dict:
                if linkage in tmp_dict[second_word]:
                    if not change_sketch_entry(tmp_dict[second_word][linkage],
                                               second_word, second_word_pos,
                                               first_word, first_word_pos, 2):
                        add_sketch_entry(second_word, second_word_pos,
                                         first_word, first_word_pos, 2)
                else:
                    add_new_linkage(second_word, second_word_pos,
                                    first_word, first_word_pos, 2)
            if first_word not in tmp_dict:
                create_sketch_entry(first_word, first_word_pos,
                                    second_word, second_word_pos, 1)
            if second_word not in tmp_dict:
                create_sketch_entry(second_word, second_word_pos,
                                    first_word, first_word_pos, 2)

    def retrieve_candidates(self, path):
        """The function for retrieving candidates for sketches"""
        for infos in self.reading_conll():
            for info_1 in infos:
                for info_2 in infos:
                    if info_1[0] == info_2[3]:
                        self.corpus_size += 1
                        # print (info_1[1], info_1[2], info_2[1], info_2[2], info_2[4])
                        self.add_new_sketch_entry(info_1[1],    # first word # todo lemmatization
                                                  info_1[2],    # part of speech of a first word
                                                  info_2[1],    # second word # todo lemmatization
                                                  info_2[2],    # part of speech of a second word
                                                  info_2[4])    # type of a linkage

    def create_candidates_dict(self, dict, word, linkage, arr):
        """The function for creating any dictionaries with sketch entries grouped by words and linkages"""
        if word in dict:
            if linkage in dict[word]:
                dict[word][linkage] += arr  # add candidates
            else:
                dict[word][linkage] = arr   # add linkage + candidates
        else:
            dict[word] = {linkage: arr}     # add word + linkage + candidates

    def filtering(self):
        """The function for filtering linkages for every part of speech"""

        def filter_pos(pos, possible_pos, obj, word, linkage):
            """The function for filter linkages by a given part of speech"""
            if obj.first_word_pos == pos:
                if obj.second_word_pos in possible_pos:
                    self.create_candidates_dict(self.filtered_candidates, word, linkage, [obj])

        # todo trigrams
        for word in self.ranged_candidates:
            for linkage in self.ranged_candidates[word]:
                for obj in self.ranged_candidates[word][linkage]:
                    # Filtering for nouns
                    possible_noun = ['ADJ', 'ADV', 'VERB']
                    filter_pos('NOUN', possible_noun, obj, word, linkage)
                    # Filtering for adjectives
                    possible_adj = ['ADV', 'ADJ', 'NOUN']
                    filter_pos('ADJ', possible_adj, obj, word, linkage)
                    # Filtering for verbs
                    possible_verb = ['ADV', 'NOUN']
                    filter_pos('VERB', possible_verb, obj, word, linkage)
                    # Filtering for adverbs
                    possible_adv = ['VERB', 'ADV', 'NOUN', 'ADJ']
                    filter_pos('ADV', possible_adv, obj, word, linkage)
                    # Filtering for conjunctions
                    possible_conj = []
                    filter_pos('CONJ', possible_conj, obj, word, linkage)
                    # Filtering for adpositions
                    possible_adp = []
                    filter_pos('ADP', possible_adp, obj, word, linkage)
                    # Filtering for particles
                    possible_part = ['VERB']
                    filter_pos('PART', possible_part, obj, word, linkage)

    def count_association_measure(self):
        """The function for counting a chosen association measure"""
        get_contingency_table(self.candidates, self.corpus_size)
        # Ranging candidates and saving the ranged candidates as an attribute
        for ranged_candidates, linkage, word in ranging(self.candidates):
            self.create_candidates_dict(self.ranged_candidates, word, linkage, ranged_candidates)
        self.filtering()

        # Testing
        print (self.filtered_candidates)
        for word in self.filtered_candidates:
            print ('WORD', word)
            for link in  self.filtered_candidates[word]:
                print ('LINKAGE', link)
                for obj in self.filtered_candidates[word][link]:
                    print (obj.first_word,
                           obj.first_word_pos,
                           obj.second_word,
                           obj.second_word_pos,
                           obj.linkage,
                           obj.head,
                           obj.abs_freq,
                           obj.dice)
            print ('='*30)


class SketchEntry:
    """The class of sketch entry which creates entries for sketches used in Russian sketches class"""

    def __init__(self, first_word, first_word_pos, second_word, second_word_pos, linkage, head):
        """Attrbutes of the SketchEntry class"""
        self.first_word = first_word            # first word text
        self.first_word_pos = first_word_pos    # part of speech of a first word
        self.second_word = second_word          # second word text
        self.second_word_pos = second_word_pos  # part of speech of a second word
        self.linkage = linkage                  # type of a linkage
        self.head = head                        # 1 - first word is a head word, 2 - second word is a head word
        self.abs_freq = 0                       # absolute frequency of the first word - second word collocation
        self.dice = 0                           # dice coefficient of the first word - second word collocation

    # Rewrite ==, !=, <, >, <=, >= python functions for proper sorting of sketches
    def __eq__(self, other):
        return self.dice == other.dice

    def __ne__(self, other):
        return self.dice != other.dice

    def __lt__(self, other):
        return self.dice < other.dice

    def __gt__(self, other):
        return self.dice > other.dice

    def __le__(self, other):
        return self.dice <= other.dice

    def __ge__(self, other):
        return self.dice >= other.dice

"""The main function which calling the RussianSketches class"""
if __name__ == '__main__':
    rs = RussianSketches()
    rs.retrieve_candidates(path)
    rs.count_association_measure()