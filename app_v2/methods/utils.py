from app_v2.graph import Task
from typing import List


def compute_station_time(station: List[Task]) -> int:
    """Computes the time that a station needs to complete all its tasks"""
    
    station_time = 0

    # an empty station has station time 0
    if not len(station):
        return station_time
    
    # TODO: modeling the last task as the predecessor of the first task should
    # allow a single function to compute all processing times and setups at once.
    for station_index, task in enumerate(station):
        
        if station_index == 0:
            # task is first in station: only use its own processing time
            station_time += task.processing_time

        elif station_index == len(station)-1:
            # task is last in station
            predecessor = station[station_index - 1]
            successor = station[0]
            station_time += task.processing_time + predecessor.setup_times[task.id] + task.setup_times[successor.id]

        else:
            # task is in between
            predecessor = station[station_index - 1]
            station_time += task.processing_time + predecessor.setup_times[task.id]
                
    return station_time


def find_station_candidates(candidate_list: List[Task], station: List[Task], cycle_time: int) -> List[Task]:
    """Check if any task in the candidate list fulfills all precedence relations and fits in actual open station"""

    # Get the tasks that have no precedence relations
    station_candidates = [task for task in candidate_list if not task.has_predecessors()]
    
    # Remove tasks that do not fit in the current station
    for task in station_candidates:
        station_time = compute_station_time(station + [task])
        if station_time >= cycle_time:
            station_candidates.remove(task)

    return station_candidates
