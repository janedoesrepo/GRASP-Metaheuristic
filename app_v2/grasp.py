import copy
import random
from app_v2.station import Station
from .local_search import improve_solution
from app_v2.graph import GraphInstance
from app_v2.task import Task
from typing import List


def calculate_greedy_index(candidate_tasks: List[Task], current_station: Station) -> List[float]:
    """Calculate the greedy index g() for all candidate tasks with respect to the current station"""

    if current_station.empty():
        return [1 / task.processing_time for task in candidate_tasks]
    else:
        last_task = current_station.last()
        return [
            1 / (task.processing_time + last_task.setup_times[task.id])
            for task in candidate_tasks
        ]


def construct_solution(instance: GraphInstance, alpha: float) -> List[Station]:

    # get a mutable copy of the original task list
    candidate_list = copy.deepcopy(instance.tasks)

    # Initialise solution with one empty station
    current_station = Station()
    stations = [current_station]
    
    while len(candidate_list):

        # Condition 1: candidates are tasks that have no precedence relations
        candidate_tasks = [
            task for task in candidate_list if not task.has_predecessors()
        ]

        # Condition 2: tasks fit into the current station
        candidate_tasks = [
            task
            for task in candidate_tasks
            if current_station.fits_task(task, instance.cycle_time)
        ]

        # if there are no candidates for the current station open a new empty station
        if not len(candidate_tasks):
            stations.append(Station())
            current_station = stations[-1]
            continue

        # compute the greedy-Index g() for each candidate task
        greedy_index = calculate_greedy_index(candidate_tasks, current_station)

        # Compute threshold function
        gmax = max(greedy_index)
        gmin = min(greedy_index)
        threshold = gmin + alpha * (gmax - gmin)

        # Find candidates that pass the threshold condition
        restricted_candidates = [
            task
            for (idx, task) in enumerate(candidate_tasks)
            if greedy_index[idx] <= threshold
        ]

        # next task to be sequenced is picked randomly from the restricted candidate list
        chosen_task = random.choice(restricted_candidates)

        # assign the chosen task to the current station and remove it from candidate list
        current_station.add_task(chosen_task)
        candidate_list.remove(chosen_task)

        # Remove the chosen task as a predecessor from all other candidates
        for task in candidate_list:
            if chosen_task.id in task.predecessors:
                task.predecessors.remove(chosen_task.id)

    return stations


def run_grasp(instance: GraphInstance, num_iter: int = 5, alpha: float = 0.3) -> List[Station]:
    """Apply Greedy Randomized Search Procedure (GRASP)"""

    for iteration in range(1, num_iter + 1):

        constructed_solution = construct_solution(instance, alpha)
        improved_solution = improve_solution(constructed_solution, instance.cycle_time)

        # the best solution has the lowest number of stations
        if iteration == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return best_solution
