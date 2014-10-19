import multiprocessing as multi
from multiprocessing import Manager, pool, freeze_support

freeze_support()
manager = Manager()

glob_data= manager.list([])

def func(a):
    glob_data.append(a)

map(func,range(10))
print glob_data  #[0,1,2,3,4 ... , 9]  Good.

p=multi.Pool(processes=8)
p.map(func,range(80))

print glob_data  # Super Good.