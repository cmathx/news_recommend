# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

f = open( 'data/train_data.txt', 'r' )
lines = f.readlines()
f.close()

f = open( 'data/train_data.edit.txt', 'w' )
for line in lines:
    f.write( line.replace('\xef\xbb\xbf','') )
f.close()

print('finished')
