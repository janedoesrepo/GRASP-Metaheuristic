from copy import deepcopy
import numpy as np
from .utils import get_candidates, assign_task
from .local_search import improve_solution


def run_grasp(instance, num_iter=5, alpha=0.3):
    """ Apply Greedy Randomized Search Procedure (GRASP) """

    constructed_solutions = []
    improved_solutions = []

    for i in range(1, num_iter+1):
        # Construct a solution and save it to the list of all constructed solutions
        print(f"\tConstructing solution {i}")
        constructed_solution = construct_solution(instance, alpha)
        constructed_solutions.append(constructed_solution)

        # Improve the constructed solution and save it to the list of all improved solutions
        print(f"\tImproving solution {i}")
        improved_solution = improve_solution(constructed_solution, instance)
        improved_solutions.append(improved_solution)

        if i == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return best_solution


def construct_solution(instance, alpha):

    candidate_list = instance.task_ids.copy()
    relations = deepcopy(instance.relations)

    # Initialise solution with one empty station
    stations = [[]]
    curr_station = stations[-1]

    n = 1
    while candidate_list:  # while cl is not empty

        # Build candidate list of iteration n (CL_n)
        station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

        if not station_candidates:
            stations.append([])
            curr_station = stations[-1]
            station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

        # print(f"Candidate list for station: {station_candidates}")

        # compute Greedy-Index g() for tasks in CL_n
        greedy_index = get_greedy_index(station_candidates, curr_station, instance.processing_times, instance.setups)

        # Compute threshold function
        gmax, _ = max(greedy_index)
        gmin, _ = min(greedy_index)
        threshold = gmin + alpha * (gmax - gmin)
        # print(f"Threshold: {threshold}")

        # Build Restricted Candidate List
        restricted_candidates = [greedy_index[i][1] for i in range(len(station_candidates)) if greedy_index[i][0] <= threshold]

        # print(f"Candidates for station under restriction: {restricted_candidates}")

        """Return random integers from the “discrete uniform” distribution of the specified dtype in the “half-open”
            interval [low, high). If high is None (the default), then results_new are from [0, low)."""
        task = np.random.choice(restricted_candidates)
        # task = restricted_candidates[np.random.randint(len(restricted_candidates))]
        # print("Aufgabe %d hinzugefügt" % task)

        # add random task from restricted_candidates to actual open station
        assign_task(curr_station, task, candidate_list, relations)

        # next iteration
        n += 1

    return stations


def get_greedy_index(station_candidates, curr_station, processing_times, setups):
    """compute greedy index g() for all task in station_candidates with respect to the curr_station"""

    greedy = []
    for candidate in station_candidates:

        if not curr_station:
            total_time = processing_times[candidate]
            # print("Sequence empty: task j =", task, "has total time t[j] =", total_time,
            #      "| computeStationTime:", computeStationTime([task], t, NONE))
        else:
            pred = curr_station[-1] # last task in sequence
            total_time = setups[pred][candidate] + processing_times[candidate]   # tsu[n][j] + t[j]
            # print("Last task", task, "has total time tsu[j][n]+t[j] =", tsu[pred][task]],
            #      "+", t[task], "=", total_time, "| computeStationTime:",
            #      computeStationTime([task], t, NONE) + tsu[pred][task]])
        value = 1 / total_time
        greedy.append((value, candidate))
        # print("Greedy Index für Aufgabe", candidate, "ist %.5f" % greedy[greedy.index((value, candidate))][0])
    return greedy

