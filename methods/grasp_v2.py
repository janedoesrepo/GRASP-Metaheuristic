from copy import deepcopy
import numpy as np
from .utils import get_candidates
from .local_search import improve_solution
from datahandler.Instance import Instance
from typing import List


def get_greedy_index(station_candidates: List[int], curr_station: List[int], processing_times: List[int], setups: List[List[int]]) -> float:
    """compute greedy index g() for all task in station_candidates with respect to the curr_station"""

    greedy = []
    for candidate in station_candidates:

        if not curr_station:
            total_time = processing_times[candidate]
        else:
            predecessor = curr_station[-1]
            total_time = setups[predecessor][candidate] + processing_times[candidate]

        value = 1 / total_time
        greedy.append((value, candidate))
        
    return greedy


def construct_solution(instance: Instance, alpha: float) -> List[List[int]]:

    # copy task ids and precedence relations
    candidate_list = instance.task_ids.copy()
    relations = deepcopy(instance.relations)

    # Initialise solution with one empty station
    stations = [[]]
    curr_station = stations[-1]

    while candidate_list:

        # try to find candidates for the current station
        station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

        # if no candidates are found, we open a new station
        if not station_candidates:
            stations.append([])
            curr_station = stations[-1]
            continue

        # compute Greedy-Index g() for station candidates
        greedy_index = get_greedy_index(station_candidates, curr_station, instance.processing_times, instance.setups)

        # Compute threshold function
        gmax, _ = max(greedy_index)
        gmin, _ = min(greedy_index)
        threshold = gmin + alpha * (gmax - gmin)

        # Find candidates that pass the threshold condition
        restricted_candidates = [greedy_index[i][1] for i in range(len(station_candidates)) if
                                 greedy_index[i][0] <= threshold]

        # add random task from restricted_candidates to actual open station
        task = np.random.choice(restricted_candidates)
        curr_station.append(task)

        # remove task for candidate list
        candidate_list.remove(task)
        
        # remove any precedence relations of that task
        # TODO: if using list comprehension, deepcopy might not be necessary
        for relation in relations:
            if task in relation:
                relation.remove(task)

    return stations


def run_grasp(instance: Instance, num_iter: int = 5, alpha: float = 0.3) -> List[List[int]]:
    """ Apply Greedy Randomized Search Procedure (GRASP) """

    # constructed_solutions = []
    # improved_solutions = []

    for iteration in range(1, num_iter+1):

        # print(f"\tConstructing solution {i}")
        constructed_solution = construct_solution(instance, alpha)
        # constructed_solutions.append(constructed_solution)

        print(f"\tImproving solution #{iteration}")
        improved_solution = improve_solution(constructed_solution, instance)
        # improved_solutions.append(improved_solution)

        # the best solution has the lowest number of stations
        if iteration == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return best_solution
