import copy
import random
from station import Station
from local_search import improve_solution
from graph import GraphInstance
from task import Task
from typing import List


def greedy(candidate_tasks: List[Task], current_station: Station) -> List[float]:
    """Calculate the greedy index g() for all candidate tasks with respect to the current station"""

    if current_station.empty():
        return [1 / task.processing_time for task in candidate_tasks]
    else:
        return [1 / (current_station.last().setup_time(task) + task.processing_time) for task in candidate_tasks]
    
    
def get_threshold(greedy_indices: List[float], alpha: float):
    gmin = min(greedy_indices)
    gmax = max(greedy_indices)
    return gmin + alpha * (gmax - gmin)


def get_candidates(candidate_list: List[Task], current_station: Station, cycle_time):
    # Condition 1: candidates are tasks that have no precedence relations
    candidates = [task for task in candidate_list if not task.has_predecessors()]

    # Condition 2: tasks fit into the current station
    return [task for task in candidates if current_station.fits_task(task, cycle_time)]
    
    
def get_restricted_candidates(candidates: List[Task], current_station: Station, alpha: float = 0.3):
    # compute the greedy-Index g() for each candidate task
    greedy_indices = greedy(candidates, current_station)

    # Compute threshold function
    threshold = get_threshold(greedy_indices, alpha)
    
    # Find candidates that pass the threshold condition
    return [task for task, greedy_index in zip(candidates, greedy_indices) if greedy_index <= threshold]


def construct_solution(candidate_list: List[Task], cycle_time: int) -> List[Station]:

    # Initialise solution with one empty station
    stations = [Station()]
    current_station = stations[-1]
    
    while len(candidate_list):

        # Find candidates for the current station
        candidates = get_candidates(candidate_list, current_station, cycle_time)
        
        # If no candidates are found then open a new empty station
        if not len(candidates):
            stations.append(Station())
            current_station = stations[-1]
            continue

        # Find candidates that fulfill a threshold condition
        restricted_candidates = get_restricted_candidates(candidates, current_station)        

        # next task to be sequenced is picked randomly from the restricted candidate list
        next_task = random.choice(restricted_candidates)

        # assign the next task to the current station and remove it from candidate list
        current_station.add(next_task)
        candidate_list.remove(next_task)

        # Remove the next task as a predecessor from all other candidates
        [task.remove_predecessor(next_task) for task in candidate_list if next_task.is_predecessor(task)]

    return stations


def run_grasp(instance: GraphInstance, num_iter: int = 5) -> List[Station]:
    """Apply Greedy Randomized Search Procedure (GRASP)"""

    for iteration in range(1, num_iter + 1):
        
        # get a mutable copy of the original task list
        candidate_list = copy.deepcopy(instance.tasks)
        
        constructed_solution = construct_solution(candidate_list, instance.cycle_time)
        improved_solution = improve_solution(constructed_solution, instance.cycle_time)

        # the best solution has the lowest number of stations
        if iteration == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return best_solution
