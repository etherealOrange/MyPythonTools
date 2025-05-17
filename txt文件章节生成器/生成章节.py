import os


if __name__ == '__main__':
    ls = os.listdir()
    for i in ls:
        if os.path.isfile(i) and i.endswith('.txt'):
            enterNums = 0
            chapterOrder = 1
            with open(i, 'r', encoding='utf-8') as inf,\
                open("out_"+i,'w',encoding='utf-8') as outf:
                for line in inf:
                    if line == '\n':
                        enterNums += 1
                    else:
                        if enterNums == 5 and len(line)<30:
                            outf.write(f"第{chapterOrder}章 "+line)
                            chapterOrder += 1
                        else:
                            enterNums = 0
                            outf.write(line)




