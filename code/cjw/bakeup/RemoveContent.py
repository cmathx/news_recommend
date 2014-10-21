# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def removeContent(init_file):
    length = len(init_file)
    final_file = init_file[0: length - 4] + "(no content).txt"
    fp_init = open(init_file, 'r')
    fp_final = open(final_file, 'w')
    for line in fp_init:
        tup = line.split('\t')
        fp_final.write('%s\t%s\t%s\t%s\t%s\n' %(tup[0], tup[1], tup[2], tup[3], tup[4]))

if __name__ == '__main__':
    init_file = '../../data/total_set.txt'
    removeContent(init_file)