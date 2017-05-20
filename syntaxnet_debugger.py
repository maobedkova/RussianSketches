path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'
syntaxnet_file = 'parsed_syntaxnet_tiny.conll'

f = open(path + syntaxnet_file, 'r', encoding='utf-8')

with open(path + 'changed_syntaxnet.conll', 'w', encoding='utf-8') as w:
    mem_line = ''
    mark = 0
    for line in f:
        if len(line) == 1:
            mark += 1
            if mark > 3:
                mem_line = ''
                mark = 1
            else:
                w.write(line)
        else:
            if line.split('\t')[0] == '1':
                mark += 1
                mem_line = line
            else:
                if mark == 1 or mark == 2:
                    mark = 0
                    w.write(mem_line)
                    w.write(line)
                elif mark == 0:
                    w.write(line)


