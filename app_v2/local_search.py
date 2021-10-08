from app_v2.graph import GraphInstance, Task
import random
from .utils import compute_station_time
from typing import List


def reassemble(sequence: List[Task], cycle_time: int) -> List[List[Task]]:
    """Reassemble a list of tasks into a list of stations. A sequence is reassembled
    by assigning its tasks one by one to a station as long as the station does not
    exceed the cycle time. Once it does, open a new station and continue assigning."""

    # print(f"Reassembling sequence: {sequence}")
    solution: List[List[Task]] = [[]]
    current_Station = solution[-1]

    for task in sequence:
        if compute_station_time(current_Station + [task]) <= cycle_time:
            current_Station.append(task)
        else:
            solution.append([task])
            current_Station = solution[-1]

    return solution


def balanced_objective(solution: List[List[Task]], cycle_time: int) -> float:
    """MINIMIZE the objective to create solutions with balanced workload"""
    result = 0
    for station in solution:
        result += pow((compute_station_time(station) / cycle_time), 2)
    return result


def imbalanced_objective(
    solution: List[List[Task]], cycle_time: int, eps: float = 0.001
) -> float:
    """MAXIMIZE the objective to create imbalanced solutions"""
    result = 0
    for station in solution:
        result += pow((cycle_time - compute_station_time(station) + eps), -1)
    return result


def balanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return x - y


def imbalanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return y - x


def improve_solution(
    solution: List[List[Task]],
    instance: GraphInstance,
    probability_threshold: float = 0.75,
) -> List[List[Task]]:
    """Try to improve a solution by exchanging the position of tasks"""

    flattened_solution = [task for station in solution for task in station]
    num_tasks = len(flattened_solution)
    # print(f"Sequence pi: {flattened_solution}")

    current_sequence = flattened_solution.copy()

    while True:

        feasible_exchanges = {}

        # choose balanced workload objective function with probability threshold
        if random.random() <= probability_threshold:
            objective_function = balanced_objective
            variation_function = balanced_variation
        else:
            objective_function = imbalanced_objective
            variation_function = imbalanced_variation

        # initialise current solution
        current_solution = reassemble(current_sequence, instance.cycle_time)
        current_solution_value = objective_function(
            current_solution, instance.cycle_time
        )
        current_solution_m = len(current_solution)

        """Iterate over all tasks but the last one and check
        if an exchange with a task on the right is feasible"""
        for i in range(num_tasks - 1):
            left_task = current_sequence[i]

            for j in range(i + 1, num_tasks):
                right_task = current_sequence[j]

                """Checks for feasability of the exchange"""
                if left_task.id in right_task.predecessors:
                    # exchange with the right task and all tasks >j unfeasible
                    # we do not need to check any of them. -> escape j-loop
                    break

                # check if any task between the both is a predecessor of the right task
                for middle_task in current_sequence[i + 1 : j]:
                    if middle_task.id in right_task.predecessors:
                        # exchange with the right task unfeasible. -> increment j
                        break

                else:
                    """The exchange itself"""
                    modified_sequence = current_sequence.copy()
                    modified_sequence[i] = right_task
                    modified_sequence[j] = left_task
                    modified_solution = reassemble(
                        modified_sequence, instance.cycle_time
                    )

                    # add indices of task left and right to the dict of feasible exchanges
                    # and save the objective function value f() and the number of stations
                    mod_sol_value = objective_function(
                        modified_solution, instance.cycle_time
                    )

                    feasible_exchanges[(i, j)] = {
                        "m": len(modified_solution),
                        "var": variation_function(
                            mod_sol_value, current_solution_value
                        ),
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

    return reassemble(current_sequence, instance.cycle_time)
