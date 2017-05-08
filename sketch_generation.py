import copy
from association_measures import get_contingency_table

path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'sketch_test.conll'

class RussianSketches:
    """Attrbutes of the RussianSketches class"""
    def __init__(self):
        self.candidates = {}
        self.corpus_size = 0    # number of bigrams

    """The function for reading conll files"""
    def reading_conll(self):
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

    """The function for adding new sketch candidates in a dictionary"""
    def add_new_sketch_entry(self, first_word, second_word, linkage):
        # print (first_word, second_word, linkage)

        """The function for creating a new sketch entry"""
        def create_sketch_entry(first_word, second_word, head, linkage=linkage):
            sl = SketchLine(first_word, second_word, linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word] = {linkage: [sl]}

        """The function for adding a new sketch entry"""
        def add_sketch_entry(first_word, second_word, head, linkage = linkage):
            sl = SketchLine(first_word, second_word, linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word][linkage] += [sl]

        """The function for changing a sketch entry"""
        def change_sketch_entry(info, first_word, second_word, head, linkage = linkage):
            for obj in info:
                if first_word == obj.first_word and second_word == obj.second_word and \
                                linkage == obj.linkage and obj.head == head:
                    obj.abs_freq += 1
                    return True

        """The function for adding a new linkage"""
        def add_new_linkage(first_word, second_word, head, linkage = linkage):
            sl = SketchLine(first_word, second_word, linkage, head)
            sl.abs_freq = 1
            self.candidates[first_word][linkage] = [sl]

        # Check if it is the first entry
        if not self.candidates:
            create_sketch_entry(first_word, second_word, 1)
            create_sketch_entry(second_word, first_word, 2)
        # Change existing sketch entries
        else:
            tmp_dict = copy.deepcopy(self.candidates)
            if first_word in tmp_dict:
                if linkage in tmp_dict[first_word]:
                    if not change_sketch_entry(tmp_dict[first_word][linkage], first_word, second_word, 1):
                        add_sketch_entry(first_word, second_word, 1)
                else:
                    add_new_linkage(first_word, second_word, 1)
            if second_word in tmp_dict:
                if linkage in tmp_dict[second_word]:
                    if not change_sketch_entry(tmp_dict[second_word][linkage], second_word, first_word, 2):
                        add_sketch_entry(second_word, first_word, 2)
                else:
                    add_new_linkage(second_word, first_word, 2)
            if first_word not in tmp_dict:
                create_sketch_entry(first_word, second_word, 1)
            if second_word not in tmp_dict:
                create_sketch_entry(second_word, first_word, 2)

    """The function for retrieving candidates for sketches"""
    def retrieve_candidates(self, path):
        print ('=== Candidate retrieval ===')
        for infos in self.reading_conll():
            for info_1 in infos:
                for info_2 in infos:
                    if info_1[0] == info_2[3]:
                        self.corpus_size += 1
                        self.add_new_sketch_entry(info_1[1],    # first word # todo lemmatization
                                                  info_2[1],    # second word # todo lemmatization
                                                  info_2[4])    # type of a linkage

    """The function for counting a chosen association measure"""
    def count_association_measure(self):
        get_contingency_table(self.candidates, self.corpus_size)

        # Testing
        print (self.candidates)
        for word in self.candidates:
            print ('WORD', word)
            for link in  self.candidates[word]:
                print ('LINKAGE', link)
                for obj in self.candidates[word][link]:
                    print (obj.first_word,
                           obj.second_word,
                           obj.linkage,
                           obj.head,
                           obj.abs_freq,
                           obj.dice)
            print ('='*30)


class SketchLine:
    """Attrbutes of the SketchLine class"""
    def __init__(self, first_word, second_word, linkage, head):
        self.first_word = first_word    # first word text
        self.second_word = second_word  # second word text
        self.linkage = linkage          # type of a linkage
        self.head = head                # 1 - first word is a head word, 2 - second word is a head word
        self.abs_freq = 0               # absolute frequency of the first word - second word collocation
        self.dice = 0                   # dice coefficient of the first word - second word collocation


"""The main function which calling the RussianSketches class"""
if __name__ == '__main__':
    rs = RussianSketches()
    rs.retrieve_candidates(path)
    rs.count_association_measure()