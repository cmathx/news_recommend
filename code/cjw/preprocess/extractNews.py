# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

fp_total_set = open('../data/total_set.txt', 'r')
fp_doc_set = open('../data/document.csv', 'w')
no_content_size = 0
cnt = 0
doc_dict = {}
for line in fp_total_set:
    words = line.split('\t')
    if doc_dict.has_key(words[1]) == False:
        fp_doc_set.write('%s\t%s' %(words[4], words[5]))
        if words[5][0] == 'N':
            no_content_size += 1
        doc_dict[words[1]] = cnt
        cnt += 1
fp_doc_set.close()
fp_total_set.close()
print no_content_size