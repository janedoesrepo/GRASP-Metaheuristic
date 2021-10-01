from copy import deepcopy
from datahandler.instance_v2 import Instance_v2
from methods.rules_v2 import TaskOrderingRule
from .utils import get_candidates, assign_task, compute_station_time
from abc import ABC, abstractmethod
from typing import List


class OptimizationStrategy:
    """Abstract class that describes the strategy by which the solutions are optimized"""
    @abstractmethod
    def solve_instance(self, instance: Instance_v2, ordering_rule: TaskOrderingRule) -> List:
        pass
    
    def __str__(self):
        return self.__class__.__name__
    

class StationOrientedStrategy(OptimizationStrategy):
    "Implements the station oriented optimization strategy"
    def solve_instance(self, instance: Instance_v2, ordering_rule: TaskOrderingRule) -> List:

        # copies are needed for in order to not change the original lists
        candidate_list = instance.task_ids.copy()
        relations = deepcopy(instance.relations)
        
        stations = [[]]
        curr_station = stations[-1]

        while candidate_list:

            # build candidate list for actual open station
            station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

            # if no task fits in actual open station then open new empty station and build a new candidate list
            if not station_candidates:
                stations.append([])
                curr_station = stations[-1]
                station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

            # order candidates
            station_candidates = ordering_rule.order_tasks(station_candidates, curr_station, instance)

            # assign first task in CL_n to actual open station
            assign_task(curr_station, station_candidates[0][0], candidate_list, relations)

        return stations
        

class TaskOrientedStrategy(OptimizationStrategy):
    "Implements the task oriented optimization strategy"
    def solve_instance(self, instance: Instance_v2, ordering_rule: TaskOrderingRule) -> List:

        # copies are needed for in order to not change the original lists
        candidate_list = instance.task_ids.copy()
        relations = deepcopy(instance.relations)
        
        stations = [[]]
        curr_station = stations[-1]

        while candidate_list:

            # build CL_n for TH depending only on precedence relations
            station_candidates = []
            for task in candidate_list:
                # proceed only if all predecessors have been assigned
                if not relations[task]:
                    station_candidates.append(task)

            # order candidate tasks
            station_candidates = ordering_rule.order_tasks(station_candidates, curr_station, instance)

            # assign first task in CL_n to first station it fits in
            temp_rel = relations[station_candidates[0][0]][:]
            for station in stations:
                # delete all tasks of actual station from precedence relations
                for task in station:
                    if task in temp_rel:
                        temp_rel.remove(task)

                # as soon as precedence relations of task are met, do station assignment
                if not temp_rel:
                    temp_station = station.copy()
                    temp_station.append(station_candidates[0][0])
                    if compute_station_time(temp_station, instance.processing_times,
                                            instance.setups) <= instance.cycle_time:
                        # if task fits in station, assign task and break for-loop
                        assign_task(station, station_candidates[0][0], candidate_list, relations)
                        break
            else:
                # in case for-loop did not break the task did not fit in any open station
                stations.append([])  # open new station
                curr_station = stations[-1]
                assign_task(curr_station, station_candidates[0][0], candidate_list, relations)

        return stations
