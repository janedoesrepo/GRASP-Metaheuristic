import numpy as np
from .utils import compute_station_time


def reassemble(sequence, instance):
    # print(f"Reassembling sequence: {sequence}")
    solution = [[]]
    curr_station = solution[-1]
    for task in sequence:
        temp_station = curr_station.copy()
        temp_station.append(task)
        if compute_station_time(temp_station, instance.processing_times, instance.setups) <= instance.cycle_time:
            curr_station.append(task)
        else:
            solution.append([task])
            curr_station = solution[-1]
    return solution


def f_balanced(solution, instance):
    # MINIMIZE objective to create solutions with balanced workload
    result = 0
    for station in solution:
        result += (compute_station_time(station, instance.processing_times, instance.setups) / instance.cycle_time) ** 2
    return result


def var_balanced(x, y):
    return x-y


def f_imbalanced(solution, instance, eps=0.001):
    # MAXIMIZE objective to create imbalanced solutions
    result = 0
    for station in solution:
        result += (1 / (instance.cycle_time - compute_station_time(station, instance.processing_times, instance.setups) + eps))
    return result


def var_imbalanced(x, y):
    return y-x


def improve_solution(solution, instance):

    pi = np.concatenate(solution)   # a flattened version of the solution
    num_tasks = len(pi)
    # print(f"Sequence pi: {pi}")

    # initialise current sequence
    curr_seq = pi.copy()

    # set threshold for choosing objective functions
    prob_threshold = 0.75

    while True:

        # initialise dictionary of feasible_exchanges
        feasible_exchanges = {}

        # choose balanced workload objective function with probability prob_threshold
        if np.random.random() <= prob_threshold:
            f = f_balanced
            var = var_balanced
        else:
            f = f_imbalanced
            var = var_imbalanced

        # initialise current solution
        curr_sol = reassemble(curr_seq, instance)
        curr_sol_value = f(curr_sol, instance)
        curr_sol_m = len(curr_sol)

        """ Test if exchange is feasible """
        # for all tasks instead of the last one
        for i in range(num_tasks-1):
            # compare task to all neighbours in pi which are right of it
            for j in range(i+1, num_tasks):
                neighbour = curr_seq[j]
                # if task is a predecessor of the neighbour pi[j]...
                if curr_seq[i] in instance.relations[neighbour]:
                    break
                else:
                    # check if any task n between the both is a predecessor of the neighbour
                    for n in range(i+1, j):
                        # if so: escape the n-loop
                        if curr_seq[n] in instance.relations[neighbour]:
                            # print("but task", curr_seq[n], "is a predecessors of neighbour", neighbour)
                            break
                    else:
                        # if not: switch tasks i and j
                        modified_seq = curr_seq.copy()
                        modified_seq[i] = curr_seq[j]
                        modified_seq[j] = curr_seq[i]
                        modified_sol = reassemble(modified_seq, instance)

                        # add task-indexes to dict of feasible exchanges and
                        # save objective function value f() and the number of stations
                        mod_sol_value = f(modified_sol, instance)
                        feasible_exchanges[(i, j)] = \
                            {'m': len(modified_sol),
                             'var': var(mod_sol_value, curr_sol_value),    # var is negative value if f is better
                             'seq': modified_seq.copy()}

        # create list of modified solutions that have as many or less stations than the current solution
        valid_solutions = [(val['m'], val['var'], key)
                           for (key, val) in feasible_exchanges.items()
                           if val['m'] <= curr_sol_m]

        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)

        # is best_exchange better than current_solution?
        if best_exchange[0] < curr_sol_m:
            # because it has fewer stations
            curr_seq = feasible_exchanges[best_exchange[2]]['seq'][:]
        elif best_exchange[1] < 0:
            # because it has positive variation
            curr_seq = feasible_exchanges[best_exchange[2]]['seq'][:]
        else:
            break

    return reassemble(curr_seq, instance)
