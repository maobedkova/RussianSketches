import numpy

path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'UD-all.conll'
output_file = 'raw_text.txt'

golden_standard_file = 'UD-all.conll'
udpipe_file = 'parsed_udpipe.conll'
syntaxnet_file = 'parsed_syntaxnet_tiny.conll'

def form_dataset(path):
    '''The function for writing a raw text from conll dataset'''
    print ('=== Text formation ===')
    with open(path + input_file, 'r', encoding='utf-8') as f:
        punct_mark = 0
        for line in f:
            if len(line) == 1:
                continue
            splitted = line.strip().split('\t')
            with open(path + output_file, 'a', encoding='utf-8') as w:
                # Every sentence from a new line
                if splitted[0] == '1':
                    if splitted[1] in '"(':
                        punct_mark = 1
                        w.write('\n' + splitted[1])
                    else:
                        w.write('\n' + splitted[1])
                else:
                    # Mind punctuation to form a text with right spaces
                    if splitted[1] in '")(':
                        if punct_mark == 2:
                            punct_mark = 0  # there is no opening punctuation
                            w.write(splitted[1])
                        elif punct_mark == 0:
                            punct_mark = 1  # there is an opening punctuation
                            w.write(' ' + splitted[1])
                    elif splitted[7] == 'punct':
                        w.write(splitted[1])
                    else:
                        if punct_mark == 1:
                            punct_mark = 2  # there are some words within punctuation marks
                            w.write(splitted[1])
                        else:
                            w.write(' ' + splitted[1])

def compare_parsers(golden_standard_file, udpipe_file, syntaxnet_file):
    '''The function for comparing different syntactic parsers'''

    def count_accuracy(gs_arr, sp_arr, true, false, accuracy, accuracy_rel):
        """The function for counting an accuracy score for every sentence and on the whole"""
        rel = 0
        rel_head = 0
        for i in range(0, len(gs_arr)):
            if gs_arr[i] == sp_arr[i]:
                true += 1
                rel += 1
                rel_head += 1
                if gs_arr[i] == 0 and sp_arr[i] == 0:
                    rel_head += 1
            else:
                false += 1
        accuracy_rel.append(float(rel_head) / len(gs_arr))
        accuracy.append(float(rel) / len(gs_arr))
        return true, false, accuracy, accuracy_rel

    def find_equivalent_line(n, mark, sp, gs, sp_line, gs_line, sp_arr, gs_arr, true, false, accuracy, accuracy_rel):
        """The function for finding equivalent lines in the golden standard and in a parser output"""
        if (len(sp_line) == 1 or sp_line.startswith('#')) or len(gs_line) == 1:
            if len(gs_line) == 1:
                if gs_arr != []:
                    true, false, accuracy, accuracy_rel = count_accuracy(gs_arr, sp_arr,
                                                                true, false,
                                                                accuracy, accuracy_rel)
                    print (true, false, accuracy)
                gs_arr = []
                sp_arr = []
                n = 0
                sp = gs
        else:
            gs_splitted = gs_line.strip().split('\t')
            sp_splitted = sp_line.strip().split('\t')
            if gs_splitted[1] == sp_splitted[1] and gs == sp:
                # print ('GOT!', gs_splitted[1], sp_splitted[1], gs, sp)
                gs_arr.append(gs_splitted[6])
                sp_arr.append(sp_splitted[6])
                sp += 1
                n = 1
                mark += 1
        return n, mark, sp, gs_arr, sp_arr, true, false, accuracy, accuracy_rel

    # Different UDpipe scores
    ud_true = 0
    ud_false = 0
    ud_accuracy = []
    ud_accuracy_rel = []
    # Different SyntaxNet scores
    sn_true = 0
    sn_false = 0
    sn_accuracy = []
    sn_accuracy_rel = []
    # Golden standard, UDpipe and SyntaxNet arrays
    gs_sn_arr = []
    gs_ud_arr = []
    ud_arr = []
    sn_arr = []

    print ('=== Looking through the files ===')
    # Opening the golden standard
    n = 0
    gs = 0
    ud = 0
    sn = 0
    with open(path + golden_standard_file, 'r', encoding='utf-8') as gs_file:
        for gs_line in gs_file:
            mark = 0
            # print ('==NEW GS==')
            # Comparison of the golden standard with UDpipe
            with open(path + udpipe_file,  'r', encoding='utf-8') as ud_file:
                # print ('UD!')
                for ud_line in ud_file:
                    n, mark, ud, \
                    gs_ud_arr, ud_arr, \
                    ud_true, ud_false, \
                    ud_accuracy, ud_accuracy_rel = \
                        find_equivalent_line(n, mark, ud, gs,
                                             ud_line, gs_line,
                                             ud_arr, gs_ud_arr,
                                             ud_true, ud_false,
                                             ud_accuracy, ud_accuracy_rel)
                    if n == 1:
                        n = 0
                        break
            # Comparison of the golden standard with SyntaxNet
            with open(path + syntaxnet_file,  'r', encoding='utf-8') as sn_file:
                # print ('SN!')
                for sn_line in sn_file:
                    n, mark, sn, \
                    gs_sn_arr, sn_arr, \
                    sn_true, sn_false, \
                    sn_accuracy, sn_accuracy_rel = \
                        find_equivalent_line(n, mark, sn, gs,
                                             sn_line, gs_line,
                                             sn_arr, gs_sn_arr,
                                             sn_true, sn_false,
                                             sn_accuracy, sn_accuracy_rel)
                    if n == 1:
                        n = 0
                        break
            if not len(gs_line) == 1:
                gs += 1
            if mark < 2:
                gs_ud_arr = []
                gs_sn_arr = []
                ud_arr = []


    print ('=== Accuracy for UDpipe ===')
    print ('Accuracy for the whole text:', float(ud_true) / float(ud_true + ud_false))
    print ('Mean accuracy for every sentence:', numpy.mean(ud_accuracy))
    print ('Mean accuracy for every sentence with higher weight for root:', numpy.mean(ud_accuracy_rel))

    print ('=== Accuracy for SyntaxNet ===')
    print ('Accuracy for the whole text:', float(sn_true) / float(sn_true + sn_false))
    print ('Mean accuracy for every sentence:', numpy.mean(sn_accuracy))
    print ('Mean accuracy for every sentence with higher weight for root:', numpy.mean(sn_accuracy_rel))


if __name__ == '__main__':
    # form_dataset(path)
    compare_parsers(golden_standard_file, udpipe_file, syntaxnet_file)
