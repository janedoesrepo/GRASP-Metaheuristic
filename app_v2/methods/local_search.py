from app_v2.graph import GraphInstance, Task
import copy
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
        result += pow( (compute_station_time(station) / cycle_time), 2)
    return result


def imbalanced_objective(solution: List[List[Task]], cycle_time: int, eps: float = 0.001) -> float:
    """MAXIMIZE the objective to create imbalanced solutions"""
    result = 0
    for station in solution:
        result += pow( (cycle_time - compute_station_time(station) + eps), -1)
    return result


def balanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return x-y


def imbalanced_variation(x: float, y: float) -> float:
    """Calculate the difference in the objective value of two solutions"""
    return y-x


def improve_solution(solution: List[List[Task]], instance: GraphInstance, probability_threshold: float = 0.75) -> List[List[Task]]:
    """Try to improve a solution by exchanging the position of tasks"""

    flattened_solution = [task for station in solution for task in station]
    num_tasks = len(flattened_solution)
    # print(f"Sequence pi: {flattened_solution}")

    current_sequence = copy.deepcopy(flattened_solution)

    while True:

        feasible_exchanges = {}

        # choose balanced workload objective function with probability threshold
        if random.random() <= probability_threshold:
            objective_function = balanced_objective
            variation = balanced_variation
        else:
            objective_function = imbalanced_objective
            variation = imbalanced_variation

        # initialise current solution
        current_solution = reassemble(current_sequence, instance.cycle_time)
        current_solution_value = objective_function(current_solution, instance.cycle_time)
        current_solution_m = len(current_solution)

        """Iterate over all tasks but the last one and check
        if an exchange with a task on the right is feasible"""
        for i in range(num_tasks-1):
            left_task = current_sequence[i]
            
            for j in range(i+1, num_tasks):
                right_task = current_sequence[j]
                
                """Checks for feasability of the exchange"""
                if left_task.id in right_task.predecessors:
                    # exchange with the right task and all tasks >j unfeasible
                    # we do not need to check any of them. -> escape j-loop
                    break
                
                # check if any task between the both is a predecessor of the right task
                for middle_task in current_sequence[i+1:j]:
                    if middle_task.id in right_task.predecessors:
                        # exchange with the right task unfeasible. -> increment j
                        break
                
                else:
                    """The exchange itself"""
                    modified_sequence = current_sequence.copy()
                    modified_sequence[i] = right_task
                    modified_sequence[j] = left_task
                    modified_solution = reassemble(modified_sequence, instance.cycle_time)

                    # add indices of task left and right to the dict of feasible exchanges
                    # and save the objective function value f() and the number of stations
                    mod_sol_value = objective_function(modified_solution, instance.cycle_time)
                    
                    feasible_exchanges[(i, j)] = \
                        {'m': len(modified_solution),
                        'var': variation(mod_sol_value, current_solution_value),
                        'seq': modified_sequence.copy()}

        """Find the best of all exchanges"""
        # create list of modified solutions that have as many or less stations than the current solution
        valid_solutions = [(solution['m'], solution['var'], indices)
                           for (indices, solution) in feasible_exchanges.items()
                           if solution['m'] <= current_solution_m]

        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)
        best_exchange_m = best_exchange[0]
        best_exchange_variation = best_exchange[1]
        best_exchange_indicies = best_exchange[2]

        # is best_exchange better than current_solution?
        if best_exchange_m < current_solution_m:
            # because it has fewer stations
            current_sequence = feasible_exchanges[best_exchange_indicies]['seq'][:]
        elif best_exchange_variation < 0:
            # because it has positive variation
            current_sequence = feasible_exchanges[best_exchange_indicies]['seq'][:]
        else:
            break

    return reassemble(current_sequence, instance.cycle_time)

# # TODO might be faster but is not tested yet
# def improve_solution(solution, relations, t, tsu, c):
#
#     # create sequence pi
#     pi = []
#     for station in solution:
#         pi.extend(station)
#
#     # initialise current sequence
#     current_seq = pi[:]
#
#     # set threshold for choosing objective functions
#     prob = 0.75
#
#     max_iter_j = len(current_seq)
#     max_iter_i = max_iter_j - 1
#
#     optimum = False
#     while not optimum:
#         # create random number to choose objective function
#         p = random()
#         if p <= prob:
#             f = f1
#         else:
#             f = f2
#
#         """ Test if exchange is feasible """
#         # for all tasks instead of the last one
#         i = 0
#         while i < max_iter_i:
#
#             if i == 0:
#                 # initialise current solution
#                 current_sol = reassemble(current_seq, t, tsu, c)
#                 current_sol_v = f(current_sol, t, tsu, c)
#                 current_sol_m = len(current_sol)
#
#             # compare task to all neighbours in pi which are right of it
#             j = i+1
#             while j < max_iter_j:
#                 # print("i, j: %d %d" %(i, j))
#                 neighbour = current_seq[j]
#                 # if task is not a predecessor of the neighbour pi[j]...
#                 if current_seq[i] not in relations[neighbour]:
#                     # print("Task is not a predecessor of neighbour")
#                     # check if any task n between the both is a predecessor of the neighbour
#                     for n in range(i+1, j):
#                         # if so: escape the n-loop. Check next neighbour (j += 1)
#                         if current_seq[n] in relations[neighbour]:
#                             # print("but task", current_seq[n], "is a predecessors of neighbour", neighbour)
#                             j += 1
#                             break
#                     else:
#                         # print("Exchange feasible")
#                         # if not: create a new sequence
#                         modified_seq = current_seq[:]
#                         modified_seq[i] = current_seq[j]
#                         modified_seq[j] = current_seq[i]
#                         modified_sol = reassemble(modified_seq, t, tsu, c)
#                         modified_sol_m = len(modified_sol)
#
#                         if modified_sol_m < current_sol_m:
#                             # print("Less stations")
#                             current_seq = modified_seq[:]
#                             j = max_iter_j
#                             i = -1
#                         elif p <= prob and modified_sol_m == current_sol_m:
#                             if f(modified_sol, t, tsu, c) - current_sol_v < 0:
#                                 # print("Better value")
#                                 j = max_iter_j
#                                 i = -1
#                                 current_seq = modified_seq[:]
#                             else:
#                                 j += 1
#                         elif prob < p and modified_sol_m == current_sol_m:
#                             if f(modified_sol, t, tsu, c) - current_sol_v > 0:
#                                 # print("Better value")
#                                 j = max_iter_j
#                                 i = -1
#                                 current_seq = modified_seq[:]
#                             else:
#                                 j += 1
#                         else:
#                             j += 1
#                 else:
#                     # if task is a predecessor of the neighbour: escape the j-loop
#                     j = max_iter_j
#             i += 1
#         optimum = True
#     return reassemble(current_seq, t, tsu, c)
