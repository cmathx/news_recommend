# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def test1():
    print xx

def test():
    global xx
    xx = 50
    test1()

test()