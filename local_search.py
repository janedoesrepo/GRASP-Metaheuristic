import random
from station import Station
from task import Task
from typing import Callable, List, Tuple


def reassemble(sequence: List[Task], cycle_time: int) -> List[Station]:
    """Reassemble a list of tasks into a list of stations. A sequence is reassembled
    by assigning its tasks one by one to a station as long as the station does not
    exceed the cycle time. Once it does, open a new station and continue assigning."""

    solution: List[Station] = [Station(cycle_time)]
    current_station = solution[-1]

    for task in sequence:
        if current_station.fits_task(task):
            current_station.append(task)
        else:
            solution.append(Station(cycle_time))
            current_station = solution[-1]
            current_station.append(task)
            
    # [solution[-1].add_task(task)
    #  if solution[-1].fits_task(task, cycle_time)
    #  else solution.append(Station([task]))
    #  for task in sequence]

    return solution


def balanced_objective(solution: List[Station]) -> float:
    """MINIMIZE the objective to create solutions with a balanced workload"""
    return sum( pow(station.station_time / station.cycle_time, 2) for station in solution)


def imbalanced_objective(solution: List[Station], eps: float = 0.001) -> float:
    """MAXIMIZE the objective to create solutions with an imbalanced workload"""
    return sum( pow(station.cycle_time - station.station_time + eps, -1) for station in solution)


def balanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return x - y


def imbalanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return y - x


def get_objective_functions(probability_threshold: float) -> Tuple[Callable, Callable]:
    """Returns two objective functions based on a random behaviour."""
    if random.random() <= probability_threshold:
        return balanced_objective, balanced_variation
    else:
        return imbalanced_objective, imbalanced_variation


def improve_solution(solution: List[Station], cycle_time: int, probability_threshold: float = 0.75) -> List[Station]:
    """Try to improve a solution by exchanging the position of tasks"""

    # create a flattened version of the solution
    solution_sequence = [task for station in solution for task in station]
    num_tasks = len(solution_sequence)

    current_sequence = solution_sequence.copy()

    while True:

        feasible_exchanges = {}

        # Randomly choose the objective functions
        calculate_objective, calculate_variation = get_objective_functions(probability_threshold)

        # initialise current solution
        current_solution = reassemble(current_sequence, cycle_time)
        current_solution_value = calculate_objective(current_solution)
        current_solution_m = len(current_solution)

        """Iterate over all tasks but the last one and check
        if an exchange with a task on the right is feasible"""
        for i, left_task in enumerate(current_sequence):

            for j in range(i + 1, num_tasks):
                right_task = current_sequence[j]

                """Checks for feasability of the exchange"""
                if left_task.is_predecessor(right_task):
                    # exchange with the right task and all tasks >j unfeasible
                    # we do not need to check any of them. -> escape j-loop
                    break

                # check if any task between the both is a predecessor of the right task
                for middle_task in current_sequence[i + 1 : j]:
                    if middle_task.is_predecessor(right_task):
                        # exchange with the right task unfeasible. -> increment j
                        break

                else:
                    """The exchange itself"""
                    modified_sequence = current_sequence.copy()
                    modified_sequence[i] = right_task
                    modified_sequence[j] = left_task
                    modified_solution = reassemble(modified_sequence, cycle_time)

                    # add indices of task left and right to the dict of feasible exchanges
                    # and save the objective function value f() and the number of stations
                    mod_sol_value = calculate_objective(modified_solution)

                    feasible_exchanges[(i, j)] = {
                        "m": len(modified_solution),
                        "var": calculate_variation(mod_sol_value, current_solution_value),
                        "seq": modified_sequence.copy(),
                    }

        """Find the best of all exchanges"""
        # create list of modified solutions that have as many or less stations than the current solution
        valid_solutions = [
            (solution["m"], solution["var"], indices)
            for (indices, solution) in feasible_exchanges.items()
            if solution["m"] <= current_solution_m
        ]

        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)
        best_exchange_m = best_exchange[0]
        best_exchange_variation = best_exchange[1]
        best_exchange_indicies = best_exchange[2]

        # is best_exchange better than current_solution?
        if best_exchange_m < current_solution_m:
            # because it has fewer stations
            current_sequence = feasible_exchanges[best_exchange_indicies]["seq"][:]
        elif best_exchange_variation < 0:
            # because it has positive variation
            current_sequence = feasible_exchanges[best_exchange_indicies]["seq"][:]
        else:
            break

    improved_solution = reassemble(current_sequence, cycle_time)

    return improved_solution
