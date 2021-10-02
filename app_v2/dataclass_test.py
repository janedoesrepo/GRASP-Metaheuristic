from dataclasses import dataclass, field
from typing import List 

@dataclass()
class Task:
    id: int
    processing_time: int
    predecessors: List[int] = field(default_factory=list, init=False)
    setup_times: List[int] = field(default_factory=list, init=False)
    
a = Task(14, 4)
print(a)
a.predecessors.append(9)
a.predecessors.append(10)
a.predecessors.append(11)
print(a)
a.setup_times = [i for i in range(10)]
print(a)


import timeit

sts = "0,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1"
st_lst = sts.split(',')

# v1
st_int_v1 = [int(st) for st in st_lst]
print(timeit.timeit('[int(st) for st in "0,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1".split(",")]', number=640))

# v2
st_int_v2 = list(map(int, st_lst))
print(timeit.timeit('list(map(int, "0,1,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1".split(",")))', number=640))