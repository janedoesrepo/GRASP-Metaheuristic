from copy import deepcopy
import numpy as np
from .utils import get_candidates
from .local_search import improve_solution


def get_greedy_index(station_candidates, curr_station, processing_times, setups):
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


def construct_solution(instance, alpha):

    candidate_list = instance.task_ids.copy()
    relations = deepcopy(instance.relations)

    # Initialise solution with one empty station
    stations = [[]]
    curr_station = stations[-1]

    n = 1
    while candidate_list:

        station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

        if not station_candidates:
            stations.append([])
            curr_station = stations[-1]
            station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

        # compute Greedy-Index g() for station candidates
        greedy_index = get_greedy_index(station_candidates, curr_station, instance.processing_times, instance.setups)

        # Compute threshold function
        gmax, _ = max(greedy_index)
        gmin, _ = min(greedy_index)
        threshold = gmin + alpha * (gmax - gmin)

        restricted_candidates = [greedy_index[i][1] for i in range(len(station_candidates)) if
                                 greedy_index[i][0] <= threshold]

        # add random task from restricted_candidates to actual open station
        task = np.random.choice(restricted_candidates)
        curr_station.append(task)

        # remove task for candidate list and remove any precedence relations
        candidate_list.remove(task)
        # TODO when using list comprehension here then deepcopy might not be necessary
        for relation in relations:
            if task in relation:
                relation.remove(task)

        n += 1

    return stations


def run_grasp(instance, num_iter=5, alpha=0.3):
    """ Apply Greedy Randomized Search Procedure (GRASP) """

    constructed_solutions = []
    improved_solutions = []

    for i in range(1, num_iter+1):

        # print(f"\tConstructing solution {i}")
        constructed_solution = construct_solution(instance, alpha)
        constructed_solutions.append(constructed_solution)

        print(f"\tImproving solution {i}")
        improved_solution = improve_solution(constructed_solution, instance)
        improved_solutions.append(improved_solution)

        if i == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return best_solution
