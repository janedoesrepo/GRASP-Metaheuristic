from abc import ABC, abstractmethod
from datahandler.Instance import Instance
from typing import List, Tuple

#TODO: Add typehints for method parameters

class TaskOrderingRule(ABC):
    """ Abstract class that decsribes a rule by which a list of tasks should be ordered
    Using an abstract class as decribed in the Strategy Pattern has several benefits:
    - There is no more need for if/else checking of which rule to apply
    - The addition of new rules is easy
    - Cleaner implementation of the has-a TaskOrderingRule relation in Heuristic
    
    On the downside this creates some boiler-plate code. Alternatively the TaskOrderingRules
    could be written in a functional adaption of the Strategy Pattern and passed as functions.
    """      
    @abstractmethod
    def order_tasks(self, candidates, station, instance: Instance) -> List[Tuple[int, float]]:
        pass
    
    
class MaxTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time descending"""
    def order_tasks(self, candidates, station, instance: Instance) -> List[Tuple[int, float]]:
        candidate_tasks = setups_plus_processing(candidates, station, instance.setups, instance.processing_times)
        return sorted(candidate_tasks, key=lambda x: x[1], reverse=True)
    
    
class MinTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time ascending"""
    def order_tasks(self, candidates, station, instance: Instance) -> List[Tuple[int, float]]:
        candidate_tasks = setups_plus_processing(candidates, station, instance.setups, instance.processing_times)
        return sorted(candidate_tasks, key=lambda x: x[1])
    
    
class MaxSOrdering(TaskOrderingRule):
    """Orders tasks by setup time descending"""
    def order_tasks(self, candidates, station, instance: Instance) -> List[Tuple[int, float]]:
        candidate_tasks = setups_only(candidates, station, instance.setups)
        return sorted(candidate_tasks, key=lambda x: x[1], reverse=True)
    
    
class MinSOrdering(TaskOrderingRule):
    """Orders tasks by setup time ascending"""
    def order_tasks(self, candidates, station, instance: Instance) -> List[Tuple[int, float]]:
        candidate_tasks = setups_only(candidates, station, instance.setups)
        return sorted(candidate_tasks, key=lambda x: x[1])
        
        
def setups_plus_processing(cln, station, tsu, t) -> List[Tuple[int, float]]:
    lst = []
    for task in cln:
        if station:
            # time between last task assigned to the actual open station and the candidate task
            value = t[task] + tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # mean of all setup times between task an all other tasks
            value = t[task] + sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return lst


def setups_only(cln, station, tsu) -> List[Tuple[int, float]]:
    lst = []
    for task in cln:
        if station:
            # time between last task assigned to the actual open station and the candidate task
            value = tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # mean of all setup times between task an all other tasks
            value = sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return lst
