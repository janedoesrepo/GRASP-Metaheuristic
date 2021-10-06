from abc import ABC, abstractmethod
from typing import List

from app_v2.graph import GraphInstance, Task
from app_v2.methods.rules import TaskOrderingRule
from .utils import find_station_candidates, compute_station_time


class OptimizationStrategy:
    """Abstract class that describes the strategy by which the solutions are optimized"""
    @abstractmethod
    def assign_tasks(self, candidate_list: List[Task], ordering_rule: TaskOrderingRule, cycle_time: int) -> List[List[Task]]:
        pass
    
    def __str__(self):
        return self.__class__.__name__
    

class StationOrientedStrategy(OptimizationStrategy):
    """The candidate tasks will be assigned to the current station if processing the task
        does not exceed the instances cycle time. Otherwise a new station is opened."""
        
    def assign_tasks(self, candidate_list: List[Task], ordering_rule: TaskOrderingRule, cycle_time: int) -> List[List[Task]]:
        
        # initialize stations
        stations: List[List[Task]] = [[]]
        current_station = stations[-1]

        # For a solution all tasks need to be assigned to station
        while len(candidate_list):
            
            # Condition 1: tasks have no precedence relations
            station_candidates = [task for task in candidate_list if not task.has_predecessors()]
            
            # Condition 2: tasks fit into the current station
            station_candidates = [task for task in station_candidates if compute_station_time(current_station + [task]) <= cycle_time]                    

            # if there are no candidates for the current station open a new empty station
            if not len(station_candidates):
                stations.append([])
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidates = ordering_rule.order_tasks(station_candidates, current_station)
            
            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates[0][0]
            
            # assign the task to the current station RCLn and remove it from candidate list CL
            current_station.append(next_task)
            candidate_list.remove(next_task)
            
            # Remove the candidate as a predecessor from all other candidates
            for task in candidate_list:
                if next_task.id in task.predecessors:
                    task.predecessors.remove(next_task.id)

        return stations
        

class TaskOrientedStrategy(OptimizationStrategy):
    """The candidate tasks will be assigned to the first station, which
        can process a task without exceeding the instances cycle time."""
    
    def assign_tasks(self, candidate_list: List[Task], ordering_rule: TaskOrderingRule, cycle_time: int) -> List[List[Task]]:
        
        # initialize stations
        stations: List[List[Task]] = [[]]
        current_station = stations[-1]

        while len(candidate_list):

            # Condition 1: tasks have no precedence relations
            station_candidates = [task for task in candidate_list if not task.has_predecessors()]
            
            # order the list of station candidates
            ordered_candidates = ordering_rule.order_tasks(station_candidates, current_station)
            
            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates[0][0]
            
            # assign first task in CL_n to first station it fits in       
            for station in stations:
                
                station_time = compute_station_time(station + [next_task])
                
                # if task does not fit in station, check the next station
                if station_time > cycle_time:
                    continue
                
                # else no need to check further stations
                break
            
            else:
                # in case for-loop did not encounter a break-statement, else is invoked.
                # the candidate did not fit in any open station -> open a new station
                stations.append([])  # open new station
                current_station = stations[-1]

            # assign the task to the current station RCLn and remove it from candidate list CL
            current_station.append(next_task)
            candidate_list.remove(next_task)
            
            # Remove the candidate as a predecessor from all other candidates
            for task in candidate_list:
                if next_task.id in task.predecessors:
                    task.predecessors.remove(next_task.id)
            
        return stations
