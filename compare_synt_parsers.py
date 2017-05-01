path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
input_file = 'UD-all.conll'
output_file = 'raw_text.txt'

def form_dataset(path):
    with open(path + input_file, 'r', encoding='utf-8') as f:
        punct_mark = 0
        for line in f:
            if len(line) == 1:
                continue
            line = line.strip()
            splitted = line.split('\t')
            with open(path + output_file, 'a', encoding='utf-8') as w:
                if splitted[0] == '1':
                    w.write('\n' + splitted[1])
                elif splitted[1] == '"' or splitted[1] == '(':
                    if punct_mark == 0:
                        punct_mark = 1
                        w.write(' ' + splitted[1])
                    if punct_mark == 1:
                        punct_mark = 0
                        w.write(splitted[1])
                elif splitted[7] == 'punct':
                    w.write(splitted[1])
                else:
                    if punct_mark == 1:
                        w.write(splitted[1])
                    else:
                        w.write(' ' + splitted[1])

if __name__ == '__main__':
    form_dataset(path)
