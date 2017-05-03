path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'UD-all.conll'
output_file = 'raw_text.txt'

'''The function for writing a raw text from conll dataset'''
def form_dataset(path):
    print ('=== Text formation ===')
    with open(path + input_file, 'r', encoding='utf-8') as f:
        punct_mark = 0
        for line in f:
            if len(line) == 1:
                continue
            splitted = line.strip().split('\t')
            with open(path + output_file, 'a', encoding='utf-8') as w:
                '''Every sentence from a new line'''
                if splitted[0] == '1':
                    if splitted[1] in '"(':
                        punct_mark = 1
                        w.write('\n' + splitted[1])
                    else:
                        w.write('\n' + splitted[1])
                else:
                    '''Mind punctuation to form a text with right spaces'''
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

if __name__ == '__main__':
    form_dataset(path)
