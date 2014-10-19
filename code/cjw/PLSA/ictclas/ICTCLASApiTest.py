# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import ctypes
import pynlpir
pynlpir.open()
s = "欢迎科研人员、技术工程师、企事业单位与个人参与NLPIR平台的建设工作。"
# print pynlpir.segment(s)

result = pynlpir.nlpir.GetKeyWords(s, 3, True)
print result

#ParagraphProcess
result = pynlpir.nlpir.ParagraphProcess(s, True)
print result.decode("utf-8")#.encode("GBK")
print type(result)
fp_total_set = open('E://Plan-Action//CCF//news_recommend//code//data//total_set.txt', 'r')
# fp_result = open('d://temp.txt', 'w')
# for line in fp_total_set:
#     element = line.split('\t')
#     fp_result.write('%s\t%s\t%s\t%s\t' %(element[0], element[1], element[2], element[3]))
#     # news_title_split_result = pynlpir.nlpir.ParagraphProcess(element[4], True)
#     news_title_split_result = pynlpir.nlpir.GetKeyWords(element[4])
#     fp_result.write(news_title_split_result)
#     fp_result.write('\t')
#     # news_content_split_result = pynlpir.nlpir.ParagraphProcess(element[5], False)
#     fp_result.write(news_content_split_result)

#ParagraphProcessA
size = ctypes.c_int()
result = pynlpir.nlpir.ParagraphProcessA(s, ctypes.byref(size), False)
result_t_vector = ctypes.cast(result, ctypes.POINTER(pynlpir.nlpir.ResultT))
words = []
for i in range(0, size.value):
    r = result_t_vector[i]
    word = s[r.start:r.start+r.length]
    words.append((word, r.sPOS))
print words

pynlpir.close()
