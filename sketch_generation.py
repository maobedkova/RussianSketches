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
        self.bigram_corpus_size = 0     # number of bigrams in a corpus
        self.trigram_corpus_size = 0    # number of trigrams in a corpus
        self.possible_pos = {'NOUN': ['ADJ', 'ADV', 'VERB'],
                             'ADJ': ['ADV', 'ADJ', 'NOUN'],
                             'VERB': ['ADV', 'NOUN'],
                             'ADV': ['VERB', 'ADV', 'NOUN', 'ADJ'],
                             'CONJ': [],
                             'ADP': [],
                             'PART': ['VERB']
                             }          # dictionary of part of speeches that are allowed

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

        def change_entry(info, linkage=linkage,
                         first_word=first_word, first_word_pos=first_word_pos,
                         second_word=second_word, second_word_pos=second_word,
                         third_word=third_word, third_word_pos=third_word_pos):
            """The function for changing a sketch entry"""
            for obj in info:
                if first_word == obj.first_word and first_word_pos == obj.first_word_pos and \
                                second_word == obj.second_word and second_word_pos == obj.second_word_pos and \
                                third_word == obj.third_word and third_word_pos == obj.third_word_pos and \
                                linkage == obj.linkage:
                    obj.abs_freq += 1
                    return True

        # Check if it is the first entry
        if not self.candidates:
            create_entry(first_word)
            create_entry(second_word)
            if third_word:
                create_entry(third_word)
        # Changing existing sketch entries
        else:
            tmp_dict = copy.deepcopy(self.candidates)
            if first_word in tmp_dict:
                if linkage in tmp_dict[first_word]:
                    if not change_entry(tmp_dict[first_word][linkage]):
                        add_entry(first_word)
                else:
                    add_linkage(first_word)
            if second_word in tmp_dict:
                if linkage in tmp_dict[second_word]:
                    if not change_entry(tmp_dict[second_word][linkage]):
                        add_entry(second_word)
                else:
                    add_linkage(second_word)
            if third_word:
                if third_word in tmp_dict:
                    if linkage in tmp_dict[third_word]:
                        if not change_entry(tmp_dict[third_word][linkage]):
                            add_entry(third_word)
                    else:
                        add_linkage(third_word)
            if first_word not in tmp_dict:
                create_entry(first_word)
            if second_word not in tmp_dict:
                create_entry(second_word)
            if third_word:
                if third_word not in tmp_dict:
                    create_entry(third_word)

    def retrieve_candidates(self, path):
        """The function for retrieving candidates for sketches"""
        for infos in self.reading_conll():
            for info_1 in infos:
                for info_2 in infos:
                    # Retrieving bigram candidates
                    if info_1[0] == info_2[3]:
                        self.bigram_corpus_size += 1
                        self.add_sketch_entry(
                            info_2[4],  # type of a linkage
                            info_1[1],  # first word # todo lemmatization
                            info_1[2],  # part of speech of a first word
                            info_2[1],  # second word # todo lemmatization
                            info_2[2]   # part of speech of a second word
                        )
                    # Retrieving trigram candidates
                    for info_3 in infos:
                        if info_1[0] == info_2[3] and info_2[0] == info_3[3]:
                            self.trigram_corpus_size += 1
                            self.add_sketch_entry(
                                info_1[2] + '_' + info_2[2] + '_' + info_3[2],  # type of a linkage
                                info_1[1],  # first word # todo lemmatization
                                info_1[2],  # part of speech of a first word
                                info_2[1],  # second word # todo lemmatization
                                info_2[2],  # part of speech of a second word
                                info_3[1],  # third word # todo lemmatization
                                info_3[2]   # part of speech of a third word
                            )

    def filtering(self):
        """The function for filtering linkages for every part of speech"""

        def create_candidates_dict(dict, word, linkage, arr):
            """The function for creating any dictionaries with sketch entries grouped by words and linkages"""
            if word in dict:
                if linkage in dict[word]:
                    dict[word][linkage] += arr  # add candidates
                else:
                    dict[word][linkage] = arr   # add linkage + candidates
            else:
                dict[word] = {linkage: arr}     # add word + linkage + candidates

        def filter_pos(obj, word, linkage):
            """The function for filter linkages by a given part of speech"""
            if obj.first_word_pos in self.possible_pos:
                if obj.second_word_pos in self.possible_pos[obj.first_word_pos]:
                    create_candidates_dict(self.filtered_candidates, word, linkage, [obj])

        for word in self.ranged_candidates:
            for linkage in self.ranged_candidates[word]:
                for obj in self.ranged_candidates[word][linkage]:
                    filter_pos(obj, word, linkage)

    def count_association_measure(self):
        """The function for counting a chosen association measure"""
        # get_contingency_table(self.candidates, self.corpus_size)
        # Ranging candidates and saving the ranged candidates as an attribute
        # for ranged_candidates, linkage, word in ranging(self.candidates):
        #     self.create_candidates_dict(self.ranged_candidates, word, linkage, ranged_candidates)
        # self.filtering()

        # Testing
        print (self.candidates)
        for word in self.candidates:
            print ('WORD', word)
            for link in  self.candidates[word]:
                print ('LINKAGE', link)
                for obj in self.candidates[word][link]:
                    print (obj.first_word,
                           obj.first_word_pos,
                           obj.second_word,
                           obj.second_word_pos,
                           obj.third_word,
                           obj.third_word_pos,
                           obj.linkage,
                           obj.abs_freq,
                           obj.dice)
            print ('='*30)


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