# # __author__ = 'cjweffort'
# # -*- coding: utf-8 -*-
#
# import multiprocessing
# import time
#
# # def test():
# #     return cnt
#
# def do_calculation(data, more):
#     cnt = 0
#     for i in xrange(100000000):
#         cnt += 1
#     return data*2 + more + cnt
#
# def start_process():
#     print 'Starting',multiprocessing.current_process().name
#
# if __name__=='__main__':
#     start = time.time()
#     for i in xrange(10):
#         print do_calculation(i, 2 * i)
#     print 'it costs:', time.time() - start
#
#     inputs1=list(range(10))
#     inputs2=list(range(10))
#     print 'Inputs  :',inputs1, inputs2
#
#     inputs = []
#     for i in xrange(10):
#         inputs.append((i, 2 * i))
#     # global cnt
#     # cnt = 0
#     # for i in xrange(1000000):
#     #     cnt += 1
#     start = time.time()
#     builtin_output=map(do_calculation,inputs1, inputs2)
#     print 'Build-In :', builtin_output
#     print 'it costs:', time.time() - start
#
#
#     pool_size=multiprocessing.cpu_count()*2
#     pool=multiprocessing.Pool(processes=pool_size,
#         initializer=start_process,)
#
#     start = time.time()
#     pool_outputs=pool.map(do_calculation,inputs1, inputs2)
#     pool.close()
#     pool.join()
#
#     print 'Pool  :',pool_outputs
#     print 'it costs:', time.time() - start

import itertools
from multiprocessing import Pool, freeze_support

def func(a, b):
    print a, b

def func_star(a_b):
    """Convert `f([1,2])` to `f(1,2)` call."""
    return func(*a_b)

def main():
    pool = Pool()
    a_args = [1,2,3]
    second_arg = 1
    pool.map(func_star, itertools.izip(a_args, itertools.repeat(second_arg)))

if __name__=="__main__":
    # freeze_support()
    main()