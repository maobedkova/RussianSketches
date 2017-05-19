import numpy

path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'UD-all.conll'
output_file = 'raw_text.txt'

golden_standard_file = 'UD-all.conll'
udpipe_file = 'parsed_udpipe.conll'
syntaxnet_file = 'parsed_syntaxnet_tiny.conll'
rusyntax_file = 'parsed_rusyntax.conll'

def form_dataset(path):
    """The function for writing a raw text from conll dataset"""
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

def compare_parsers(golden_standard_file, udpipe_file, syntaxnet_file, rusyntax_file):
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

    def find_equivalent_line(w, n, mark, first_line_mark, sp_line, gs_line, sp_arr, gs_arr, true, false, accuracy, accuracy_rel):
        """The function for finding equivalent lines in the golden standard and in a parser output"""
        gs_splitted = gs_line.strip().split('\t')
        sp_splitted = sp_line.strip().split('\t')
        # print (gs_splitted, sp_splitted, gs, sp)
        if gs_splitted[1] == sp_splitted[1] and gs_splitted[0] == sp_splitted[0]:
            w.write ('GOT! ' + gs_splitted[1] + ' ' + sp_splitted[1])
            gs_arr.append(gs_splitted[6])
            sp_arr.append(sp_splitted[6])
            n = 1
            mark += 1
        #     first_line_mark = 0
        # else:
        #     if first_line_mark == 1:
        #         first_line_mark = 2
        return n, mark, first_line_mark, gs_arr, sp_arr, true, false, accuracy, accuracy_rel

    def writing_check(w, gs_line, gs_arr, sp_arr, true, false, accuracy, accuracy_rel, mark):
        if len(gs_line) == 1:
            if gs_arr != []:
                true, false, accuracy, accuracy_rel = count_accuracy(gs_arr, sp_arr,
                                                            true, false,
                                                            accuracy, accuracy_rel)
                w.write (str(true) + ' ' + str(false) + ' ' + str(accuracy))
                return True


    def iter_file(w, i, first_line_mark, parser_file, n, mark, gs_line,
                  arr, gs_arr, true, false, accuracy, accuracy_rel):
        """The function for iterating a parser file"""
        if writing_check(w, gs_line, gs_arr, arr, true, false, accuracy, accuracy_rel, mark):
            mark += 1
            return n, mark, first_line_mark, gs_arr, arr, true, false, accuracy, accuracy_rel

        for line in parser_file:
            # if first_line_mark == 2:
            #     break
            if not line.startswith('#'):
                if not len(line) == 1:
                    n, mark, first_line_mark,\
                    gs_arr, arr, \
                    true, false, \
                    accuracy, accuracy_rel = \
                        find_equivalent_line(w, n, mark,first_line_mark,
                                             line, gs_line,
                                             arr, gs_arr,
                                             true, false,
                                             accuracy, accuracy_rel)
            # if i > 350:
            #     w.write('!!!!' + str(first_line_mark) + ' !!!!')
            # w.write(str(first_line_mark))
            if len(gs_line) != 1 and len(line) == 1:
                # w.write('EMPTY!')
                # if first_line_mark > 1:
                #     arr = []
                #     first_line_mark = 0
                #     break
                # elif gs_line.split('\t')[0] == '1':
                #     # w.write('@MARK@')
                #     first_line_mark += 1
                if gs_line.split('\t')[0] != '1':
                    # w.write('YEEEP')
                    arr = []
                    break
                # if gs_line.split('\t')[0] == '1':
                #     first_line_mark = 1
                #     arr = []
                #     break

            if n == 1:
                n = 0
                break
            i += 1

        return n, mark, first_line_mark, gs_arr, arr, true, false, accuracy, accuracy_rel

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

    # Different RuSyntax scores
    rs_true = 0
    rs_false = 0
    rs_accuracy = []
    rs_accuracy_rel = []

    # Golden standard, UDpipe, SyntaxNet and RuSyntax arrays
    gs_sn_arr = []
    gs_ud_arr = []
    gs_rs_arr = []
    ud_arr = []
    sn_arr = []
    rs_arr = []

    n = 0
    quit_mark = 0
    first_line_mark = 0
    i = 0

    # Opening parser`s files
    ud_file = open(path + udpipe_file,  'r', encoding='utf-8')
    sn_file = open(path + syntaxnet_file,  'r', encoding='utf-8')
    rs_file = open(path + rusyntax_file,  'r', encoding='utf-8')

    # Writing down the results
    with open('parsers_results.txt', 'w', encoding='utf-8') as w:
        # Opening the golden standard
        with open(path + golden_standard_file, 'r', encoding='utf-8') as gs_file:
            for gs_line in gs_file:
                mark = 0
                if quit_mark == 1:
                    if len(gs_line) == 1:
                        quit_mark = 0
                    continue
                w.write ('==NEW GS==' + gs_line)
                # Comparison of the golden standard with UDpipe
                w.write ('UD!')
                n, mark, first_line_mark, gs_arr, ud_arr, ud_true, ud_false, ud_accuracy, ud_accuracy_rel = \
                    iter_file(w, i, first_line_mark, ud_file, n, mark, gs_line, ud_arr, gs_ud_arr,
                              ud_true, ud_false, ud_accuracy, ud_accuracy_rel)
                # Comparison of the golden standard with SyntaxNet
                w.write ('SN!')
                n, mark,first_line_mark, gs_arr, sn_arr, sn_true, sn_false, sn_accuracy, sn_accuracy_rel = \
                    iter_file(w,i, first_line_mark, sn_file, n, mark, gs_line, sn_arr, gs_sn_arr,
                              sn_true, sn_false, sn_accuracy, sn_accuracy_rel)
                # Comparison of the golden standard with RuSyntax
                w.write ('RS!')
                n, mark, first_line_mark, gs_arr, rs_arr, rs_true, rs_false, rs_accuracy, rs_accuracy_rel = \
                    iter_file(w,i, first_line_mark, rs_file, n, mark, gs_line, rs_arr, gs_rs_arr,
                              rs_true, rs_false, rs_accuracy, rs_accuracy_rel)
                if mark < 3:
                    gs_ud_arr = []
                    gs_sn_arr = []
                    gs_rs_arr = []
                    ud_arr = []
                    sn_arr = []
                    rs_arr = []
                    quit_mark = 1
                i += 1
                w.write (str(i))


        w.write('The number of sentences processed: ' + str(len(ud_accuracy)) + '\n')
        w.write('=== Accuracy for UDpipe ===\n')
        w.write('Accuracy for the whole text: ' + str(float(ud_true) / float(ud_true + ud_false)) + '\n')
        w.write('Mean accuracy for every sentence: ' + str(numpy.mean(ud_accuracy)) + '\n')
        w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(ud_accuracy_rel)) + '\n\n')
        w.write('=== Accuracy for SyntaxNet ===\n')
        w.write('Accuracy for the whole text: ' + str(float(sn_true) / float(sn_true + sn_false)) + '\n')
        w.write('Mean accuracy for every sentence: ' + str(numpy.mean(sn_accuracy)) + '\n')
        w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(sn_accuracy_rel)) + '\n')
        w.write('=== Accuracy for RuSyntax ===\n')
        w.write('Accuracy for the whole text: ' + str(float(rs_true) / float(rs_true + rs_false)) + '\n')
        w.write('Mean accuracy for every sentence: ' + str(numpy.mean(rs_accuracy)) + '\n')
        w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(rs_accuracy_rel)) + '\n')

if __name__ == '__main__':
    # form_dataset(path)
    compare_parsers(golden_standard_file, udpipe_file, syntaxnet_file, rusyntax_file)
