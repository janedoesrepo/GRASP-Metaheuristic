from app_v2.graph import GraphInstance
from typing import List


def compute_station_time(station: List[int], processing_times: List[int], setups: List[List[int]]) -> int:
    """Computes the time that a station needs to complete all its tasks"""
    
    t_station = 0

    # an empty station has station time 0
    if not station:
        return t_station
    
    # TODO: modeling the last task as the predecessor of the first task should allow a single function
    #       to compute all processing times and setups. Also the station.index() calls are relatively
    #       expensive and should be replaced.
    for task in station:
        # task is first in station: only use its own processing time
        if station.index(task) == 0:
            t_station += processing_times[task]

        # task is last in station
        elif station.index(task) == len(station)-1:
            pred = station[station.index(task) - 1]
            succ = station[0]
            t_station += processing_times[task] + setups[pred][task] + setups[task][succ]

        # task is in between
        else:
            pred = station[station.index(task) - 1]
            t_station += processing_times[task] + setups[pred][task]
                
    return t_station


def get_candidates(instance: GraphInstance, candidate_list: List[int], relations: List[List[int]], station: List[int]) -> List[int]:
    """Check if any task in the candidate_list fulfills all precedence relations and fits in actual open station"""

    station_candidates = []
    for task in candidate_list:

        # if task has predecessors it can't be sequenced
        if relations[task]:
            break

        # check if task fits in station
        if compute_station_time(station + [task], instance.processing_times, instance.setups) <= instance.cycle_time:
            station_candidates.append(task)

    return station_candidates


def assign_task(station, task, candidate_list, relations):
    station.append(task)  # Sequence random task in RCLn
    candidate_list.remove(task)  # Remove this task from CL

    # Remove this task from relations
    # TODO when using list comprehension here then deepcopy might not be necessary
    for relation in relations:
        if task in relation:
            relation.remove(task)