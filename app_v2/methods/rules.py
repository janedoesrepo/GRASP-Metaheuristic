from app_v2.graph import Task
from abc import ABC, abstractmethod
from typing import List, Tuple


class TaskOrderingRule(ABC):
    """ Abstract class that decsribes a rule by which a list of tasks should be ordered.
    
    Using an abstract class as decribed in the Strategy Pattern has several benefits:
    - There is no more need for if/else checking of which rule to apply
    - The addition of new rules is easy
    - Cleaner implementation of the has-a TaskOrderingRule relation in Heuristic
    
    On the downside this creates some boiler-plate code. Alternatively the TaskOrderingRules
    could be written in a functional adaption of the Strategy Pattern and passed as functions.
    """      
    @abstractmethod
    def order_tasks(self, candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
        pass
    
    def __str__(self):
        return self.__class__.__name__
    
    
class MaxTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time descending"""
    def order_tasks(self, candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
        candidate_tasks = setups_plus_processing(candidates, station)
        return sorted(candidate_tasks, key=lambda x: x[1], reverse=True)
    
    
class MinTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time ascending"""
    def order_tasks(self, candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
        candidate_tasks = setups_plus_processing(candidates, station)
        return sorted(candidate_tasks, key=lambda x: x[1])
    
    
class MaxSOrdering(TaskOrderingRule):
    """Orders tasks by setup time descending"""
    def order_tasks(self, candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
        candidate_tasks = setups_only(candidates, station)
        return sorted(candidate_tasks, key=lambda x: x[1], reverse=True)
    
    
class MinSOrdering(TaskOrderingRule):
    """Orders tasks by setup time ascending"""
    def order_tasks(self, candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
        candidate_tasks = setups_only(candidates, station)
        return sorted(candidate_tasks, key=lambda x: x[1])
        
        
def setups_plus_processing(candidates: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
    """TODO: list comprehension"""
    lst = []
    for task in candidates:
        if len(station):
            # time between last task assigned to the actual open station and the candidate task
            value = task.processing_time + station[-1].setup_times[task.id]
            lst.append((task, value))
        else:
            # mean of all setup times between task an all other tasks
            value = task.processing_time + sum(task.setup_times) / (len(task.setup_times)-1)
            lst.append((task, value))
            
    return lst


def setups_only(cln: List[Task], station: List[Task]) -> List[Tuple[Task, float]]:
    """TODO: list comprehension"""
    lst = []
    for task in cln:
        if len(station):
            # time between last task assigned to the actual open station and the candidate task
            value = station[-1].setup_times[task.id]
            lst.append((task, value))
        else:
            # mean of all setup times between task an all other tasks
            value = sum(task.setup_times) / (len(task.setup_times)-1)
            lst.append((task, value))
            
    return lst
