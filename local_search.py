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
        if current_station.can_fit(task):
            current_station.add_task(task)
        else:
            solution.append(Station(cycle_time))
            current_station = solution[-1]
            current_station.add_task(task)

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

def swap_tasks(sequence: List[Task], pos1: int, pos2: int) -> List[Task]:
    """Returns a new sequence with the position of two tasks swapped"""
    new_sequence = sequence.copy()
    new_sequence[pos2] = sequence[pos1]
    new_sequence[pos1] = sequence[pos2]
    return new_sequence

def improve_solution(solution: List[Station], cycle_time: int, probability_threshold: float = 0.75) -> List[Station]:
    """Try to improve a solution by exchanging the position of tasks"""

    # create a flattened version of the solution
    solution_sequence: List[Task] = [task for station in solution for task in station]
    num_tasks = len(solution_sequence)

    current_sequence = solution_sequence.copy()

    while True:
        # Container for valid solutions
        valid_solutions = []

        # Randomly choose the objective functions
        calculate_objective, calculate_variation = get_objective_functions(probability_threshold)

        # initialise current solution
        current_solution = reassemble(current_sequence, cycle_time)
        current_solution_value = calculate_objective(current_solution)
        num_stations_current = len(current_solution)

        """Iterate over all tasks but the last one and check
        if an exchange with a task on the right is feasible"""
        for i in range(num_tasks-1):

            for j in range(i + 1, num_tasks):
                right_task = current_sequence[j]

                # The exchange is feasible if right_task has no predecessors on his left in the sequence
                if any(left_task.is_predecessor(right_task) for left_task in current_sequence[i:j]):
                    break

                # Exchange the tasks and reassemble the modified sequence
                modified_sequence = swap_tasks(current_sequence, i, j)
                modified_solution = reassemble(modified_sequence, cycle_time)
                
                # Save the modified sequence if at least as good than the current one
                num_stations_modified = len(modified_solution)
                if num_stations_modified <= num_stations_current:
                    modified_solution_value = calculate_objective(modified_solution)
                    variation = calculate_variation(modified_solution_value, current_solution_value)
                    
                    valid_solutions.append(
                        (num_stations_modified, variation, (i,j))
                    )

        """Find the best of all exchanges"""

        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)
        best_exchange_m = best_exchange[0]
        best_exchange_variation = best_exchange[1]
        i, j = best_exchange[2]

        # is best_exchange better than current_solution?
        if best_exchange_m < num_stations_current:
            # because it has fewer stations
            current_sequence = swap_tasks(current_sequence, i, j)
        elif best_exchange_variation < 0:
            # because it has positive variation
            current_sequence = swap_tasks(current_sequence, i, j)
        else:
            # Current sequence can't be improved -> end while-loop
            break

    improved_solution = reassemble(current_sequence, cycle_time)

    return improved_solution
