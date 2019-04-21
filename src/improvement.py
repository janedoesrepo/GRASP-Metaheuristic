from random import random
from construction import computeStationTime


def reassemble(sequence, t, tsu, c):
    solution = [[]]
    for task in sequence:
        station = solution[-1]
        temp_station = station[:]
        temp_station.append(task)
        if computeStationTime(temp_station, t, tsu) <= c:
            # append task to actual open station
            solution[-1].append(task)
        else:
            # open new station and append task
            solution.append([task])
    return solution


# MINIMISE objective: to create solutions with balanced workload
def f1(solution, t, tsu, c):
    result = 0
    for station in solution:
        result += (computeStationTime(station, t, tsu) / c) ** 2
    return result


# MAXIMISE objective: to create imbalanced solutions
def f2(solution, t, tsu, c):
    result = 0
    eps = 0.001
    for station in solution:
        result += (1 / (c - computeStationTime(station, t, tsu) + eps))
    return result


def improveSolution(solution, relations, t, tsu, c):

    # create sequence pi
    pi = []
    for station in solution:
        pi.extend(station)

    # initialise current sequence
    current_seq = pi[:]

    # set threshold for choosing objective functions
    prob = 0.75

    while True:

        # initialise dictionary of feasible_exchanges
        feasible_exchanges = {}

        # create random number to choose objective function
        p = random()
        if p <= prob:
            f = f1
        else:
            f = f2

        # initialise current solution
        current_sol = reassemble(current_seq, t, tsu, c)
        current_sol_v = f(current_sol, t, tsu, c)
        current_sol_m = len(current_sol)

        """ Test if exchange is feasible """
        # for all tasks instead of the last one
        for i in range(len(pi)-1):
            # compare task to all neighbours in pi which are right of it
            for j in range(i+1, len(pi)):
                neighbour = current_seq[j]
                # if task is not a predecessor of the neighbour pi[j]...
                if current_seq[i] not in relations[neighbour]:
                    # check if any task n between the both is a predecessor of the neighbour
                    for n in range(i+1, j):
                        # if so: escape the n-loop
                        if current_seq[n] in relations[neighbour]:
                            # print("but task", current_seq[n], "is a predecessors of neighbour", neighbour)
                            break
                    else:
                        # if not: create a new sequence
                        modified_seq = current_seq[:]
                        modified_seq[i] = current_seq[j]
                        modified_seq[j] = current_seq[i]
                        modified_sol = reassemble(modified_seq, t, tsu, c)

                        # add task-indexes to dict of feasible exchanges and
                        # save objective function value f() and the number of stations
                        value = f(modified_sol, t, tsu, c)
                        if p <= prob:
                            feasible_exchanges[(i, j)] = {'m': len(modified_sol),
                                                          'var': value - current_sol_v,
                                                          # var is a negative value if f is better
                                                          'seq': modified_seq[:]}
                        else:
                            feasible_exchanges[(i, j)] = {'m': len(modified_sol),
                                                          # var is a negative value if f is better
                                                          'var': current_sol_v - value,
                                                          'seq': modified_seq[:]}
                else:
                    # if task is a predecessor of the neighbour: escape the j-loop
                    break

        # create list of modified solutions that have as many or less stations than the current solution
        valid_solutions = [(val['m'], val['var'], key)
                           for (key, val) in feasible_exchanges.items()
                           if val['m'] <= current_sol_m]

        # get best value in order min(m), min(var), min(key)
        best_exchange = min(valid_solutions)

        # is best_exchange better than current_solution?
        if best_exchange[0] < current_sol_m:
            # because it has fewer stations
            current_seq = feasible_exchanges[best_exchange[2]]['seq'][:]
        elif best_exchange[1] < 0:
            # because it has positive variation
            current_seq = feasible_exchanges[best_exchange[2]]['seq'][:]
        else:
            # escape the while-loop
            break

    return reassemble(current_seq, t, tsu, c)
