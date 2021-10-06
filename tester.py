from app_v2.graph import Task, GraphInstance
from app_v2.methods import heuristic
from app_v2.methods.rules import MaxTSOrdering, MinTSOrdering
from app_v2.methods.strategies import StationOrientedStrategy, TaskOrientedStrategy

from app_v1.datahandler.Instance import Instance
from app_v1.methods import Heuristic

import random
import copy
        
    

def main():
    
    
    """Create Instances"""
    appv1_instance = Instance("MITCHELL.IN2", "TS0.25", 1)
    appv1_instance.load()
    
    appv2_instance = GraphInstance("MITCHELL.IN2", "TS0.25", 1)
    appv2_instance.parse_instance()
    
    """Create Heuristics"""
    appv1_heuristic = Heuristic.Heuristic("TH", "max_ts")
    appv2_heuristic = heuristic.Heuristic(TaskOrientedStrategy(), MaxTSOrdering())
    
    """Solve instances"""
    solution1 = appv1_heuristic.apply(appv1_instance)
    print(solution1)
    
    solution2 = appv2_heuristic.solve_instance(appv2_instance)
    for station in solution2:
        print(station)
    
    # """Solve an instance"""
    # solution1 = SH_maxTSHeuristic.solve_instance(instance)
    # print(len(solution1) )
    # solution2 = heuristic.solve_instance(instance)
    # print(len(solution2))
    
    # """Test Task Creation and Removal"""
    # task1 = Task(1, random.randint(0, 10))
    # task1.predecessors = [0,3,4]
    # task2 = Task(2, random.randint(0, 10))
    # task2.predecessors = [1,3,4]
    
    # # can we remove a task from a list?
    # print("Remove task1 from list")
    # tasks = [task1, task2]
    # print(tasks)
    
    # tasks.remove(task1)
    # print(tasks)
    
    # # can we deepcopy tasks?
    # print("Make a deepcopy of task2 and remove predecessor 1")
    # task2_copy = copy.deepcopy(task2)
    # task2_copy.predecessors.remove(1) 
    # print(task2)
    # print(task2_copy)
    
    # print("Deepcopy a list of tasks and remove predecessor 3 from the first task")
    # tasks.append(task1)
    # tasks_copy = copy.deepcopy(tasks)
    # tasks_copy[0].predecessors.remove(3)
    # print(tasks)
    # print(tasks_copy)


if __name__ == '__main__':
    main()
    