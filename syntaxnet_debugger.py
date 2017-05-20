syntaxnet_file = 'parsed_syntaxnet_tiny.conll'
path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'

f = open(path + syntaxnet_file, 'r', encoding='utf-8')

with open(path + 'changed_syntaxnet.conll', 'w', encoding='utf-8') as w:
    mem_line = ''
    mark = 0
    i = 0
    for line in f:
        # w.write('\n')
        # print (line)
        if len(line) == 1:
            i += 1
            # print ('EMPTY')
            mark += 1
            if mark > 3:
                # print ('WRITTEN')
                # w.write(mem_line)
                # w.write(line)
                mem_line = ''
                mark = 1
            else:
                w.write(line)
        else:
            if line.split('\t')[0] == '1':
                # w.write('FIRST_LINE')
                # print ('FIRST LINE', mark)
                mark += 1
                mem_line = line
            else:
                # print ('ELSE', mark)
                # w.write('ELSE')
                if mark ==2 or mark == 1:
                    mark = 0
                    w.write(mem_line)
                    w.write(line)
                elif mark == 0:
                    w.write(line)

                #
                # w.write('OTHER')
                # if mark <= 1:
                #     w.write(str(mark) + mem_line)
                #     mem_line = ''
                #     w.write(str(mark) + line)
                # else:
                #     w.write(line)
                #     mark =0

                # print ('OTHER')
                # print ('WRITTEN')
        #
        # if i == 4:
        #     break

