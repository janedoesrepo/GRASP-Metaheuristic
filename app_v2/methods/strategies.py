from abc import ABC, abstractmethod
from typing import List

from app_v2.graph import GraphInstance, Task
from app_v2.methods.rules import TaskOrderingRule
from .utils import find_station_candidates, compute_station_time


class OptimizationStrategy:
    """Abstract class that describes the strategy by which the solutions are optimized"""
    @abstractmethod
    def solve_instance(self, instance: GraphInstance, ordering_rule: TaskOrderingRule) -> List[List[Task]]:
        pass
    
    def __str__(self):
        return self.__class__.__name__
    

class StationOrientedStrategy(OptimizationStrategy):
    """Implements the station oriented optimization strategy"""
    def solve_instance(self, instance: GraphInstance, ordering_rule: TaskOrderingRule) -> List[List[Task]]:

        # get a mutable copy of the original task list
        candidate_list = instance.tasks.copy()
        
        # initialize stations
        stations: List[List[Task]] = [[]]
        current_station = stations[-1]

        # as long as there are tasks in the candidate list try to assign them
        while len(candidate_list):
            
            # find the candidates for the current station
            station_candidates = find_station_candidates(candidate_list, current_station, instance.cycle_time)

            # if there are no candidates for the current station open a new empty station
            if not len(station_candidates):
                stations.append([])
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidates = ordering_rule.order_tasks(station_candidates, current_station)
            candidate = ordered_candidates[0][0]
            
            # assign the candidate to the current station RCLn and remove it from candidate list CL
            current_station.append(candidate)
            candidate_list.remove(candidate)
            
            # Remove the candidate as a predecessor from all other candidates
            for task in candidate_list:
                if candidate.id in task.predecessors:
                    task.predecessors.remove(candidate.id)

        return stations
        

class TaskOrientedStrategy(OptimizationStrategy):
    """Implements the task oriented optimization strategy"""
    def solve_instance(self, instance: GraphInstance, ordering_rule: TaskOrderingRule) -> List[List[Task]]:

        # get a mutable copy of the original task list
        candidate_list = instance.tasks.copy()
        
        # initialize stations
        stations: List[List[Task]] = [[]]
        current_station = stations[-1]

        # as long as there are tasks in the candidate list try to assign them
        while candidate_list:

            # find the candidates (tasks that have no precedence relations) for the current station
            station_candidates = [task for task in candidate_list if not task.has_predecessors()]

            # order candidate tasks
            ordered_candidates = ordering_rule.order_tasks(station_candidates, current_station)
            candidate = ordered_candidates[0][0]
            
            # assign first task in CL_n to first station it fits in       
            for station in stations:
                
                # if task does not fit in station, check the next station
                station_time = compute_station_time(station + [candidate])
                if station_time >= instance.cycle_time:
                    continue
                
                # else assign candidate task in CL_n to current station RCLn and remove it from candidate list CL
                current_station.append(candidate)
                candidate_list.remove(candidate)
                
                # Remove this task as a predecessor from all other candidates
                for task in candidate_list:
                    if candidate.id in task.predecessors:
                        task.predecessors.remove(candidate.id)
                
                # the candidate was assigned. No need to check other stations
                break
            else:
                # in case for-loop did not encounter a break-statement, else is invoked.
                # the candidate did not fit in any open station -> open a new station
                stations.append([])  # open new station
                current_station = stations[-1]
                
                # assign first task in CL_n to current station RCLn and remove it from candidate list CL
                current_station.append(candidate)
                candidate_list.remove(candidate)
                
                # Remove this task as a predecessor from all other candidates
                for task in candidate_list:
                    if candidate.id in task.predecessors:
                        task.predecessors.remove(candidate.id)

        return stations
