import copy
import random
from typing import Callable

from sualbsp_solver.data_model import Station, TaskList


def balanced_objective(solution: list[Station]) -> float:
    """MINIMIZE the objective to create solutions with a balanced workload"""
    return sum(
        pow(station.station_time / station.cycle_time, 2) for station in solution
    )


def imbalanced_objective(solution: list[Station], eps: float = 0.001) -> float:
    """MAXIMIZE the objective to create solutions with an imbalanced workload"""
    return sum(
        pow(station.cycle_time - station.station_time + eps, -1) for station in solution
    )


def balanced_variation(objective1: float, objective2: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return objective1 - objective2


def imbalanced_variation(objective1: float, objective2: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return objective2 - objective1


def get_objective_functions(probability_threshold: float) -> tuple[Callable, Callable]:
    """Returns two objective functions based on a random behaviour."""
    if random.random() <= probability_threshold:
        return balanced_objective, balanced_variation
    else:
        return imbalanced_objective, imbalanced_variation


def improve_solution(
    solution: list[Station], cycle_time: int, probability_threshold: float = 0.75
) -> list[Station]:
    """Try to improve a solution by exchanging the position of tasks."""

    # create a flattened version of the solution
    solution_sequence = TaskList.from_solution(solution)
    num_tasks = len(solution_sequence)

    current_sequence = copy.copy(solution_sequence)

    while True:
        # Container for valid solutions
        valid_solutions = []

        # Randomly choose the objective functions
        calculate_objective, calculate_variation = get_objective_functions(
            probability_threshold
        )

        # initialise current solution
        current_solution = current_sequence.reassemble(cycle_time)
        current_solution_value = calculate_objective(current_solution)
        num_stations_current = len(current_solution)

        """Iterate over all tasks but the last one and check
        if an exchange with a task on the right is feasible"""
        for i in range(num_tasks - 1):

            for j in range(i + 1, num_tasks):
                right_task = current_sequence[j]

                # The exchange is feasible if right_task has no predecessors on his left in the sequence
                if any(
                    left_task.is_predecessor_of(right_task)
                    for left_task in current_sequence[i:j]
                ):
                    print(f">>> Task {right_task} has predecessory")
                    break

                # Exchange the tasks and reassemble the modified sequence
                modified_sequence = current_sequence.swap_tasks(i, j)
                modified_solution = modified_sequence.reassemble(cycle_time)

                # Save the modified sequence if at least as good than the current one
                num_stations_modified = len(modified_solution)
                if num_stations_modified <= num_stations_current:
                    modified_solution_value = calculate_objective(modified_solution)
                    variation = calculate_variation(
                        modified_solution_value, current_solution_value
                    )

                    valid_solutions.append((num_stations_modified, variation, (i, j)))

        """Find the best of all exchanges"""
        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)
        best_exchange_m = best_exchange[0]
        best_exchange_variation = best_exchange[1]
        i, j = best_exchange[2]

        # is best_exchange better than current_solution?
        has_fewer_stations = best_exchange_m < num_stations_current
        has_positive_variation = best_exchange_variation < 0

        if has_fewer_stations | has_positive_variation:
            current_sequence = current_sequence.swap_tasks(i, j)
        else:
            # Current sequence can't be improved -> end while-loop
            break

    improved_solution = current_sequence.reassemble(cycle_time)

    return improved_solution
