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

    max_iter_j = len(current_seq)
    max_iter_i = max_iter_j - 1

    optimum = False
    while not optimum:
        # create random number to choose objective function
        p = random()
        if p <= prob:
            f = f1
        else:
            f = f2

        """ Test if exchange is feasible """
        # for all tasks instead of the last one
        i = 0
        while i < max_iter_i:

            if i == 0:
                # initialise current solution
                current_sol = reassemble(current_seq, t, tsu, c)
                current_sol_v = f(current_sol, t, tsu, c)
                current_sol_m = len(current_sol)

            # compare task to all neighbours in pi which are right of it
            j = i+1
            while j < max_iter_j:
                # print("i, j: %d %d" %(i, j))
                neighbour = current_seq[j]
                # if task is not a predecessor of the neighbour pi[j]...
                if current_seq[i] not in relations[neighbour]:
                    # print("Task is not a predecessor of neighbour")
                    # check if any task n between the both is a predecessor of the neighbour
                    for n in range(i+1, j):
                        # if so: escape the n-loop. Check next neighbour (j += 1)
                        if current_seq[n] in relations[neighbour]:
                            # print("but task", current_seq[n], "is a predecessors of neighbour", neighbour)
                            j += 1
                            break
                    else:
                        # print("Exchange feasible")
                        # if not: create a new sequence
                        modified_seq = current_seq[:]
                        modified_seq[i] = current_seq[j]
                        modified_seq[j] = current_seq[i]
                        modified_sol = reassemble(modified_seq, t, tsu, c)
                        modified_sol_m = len(modified_sol)

                        if modified_sol_m < current_sol_m:
                            # print("Less stations")
                            current_seq = modified_seq[:]
                            j = max_iter_j
                            i = -1
                        elif p <= prob and modified_sol_m == current_sol_m:
                            if f(modified_sol, t, tsu, c) - current_sol_v < 0:
                                # print("Better value")
                                j = max_iter_j
                                i = -1
                                current_seq = modified_seq[:]
                            else:
                                j += 1
                        elif prob < p and modified_sol_m == current_sol_m:
                            if f(modified_sol, t, tsu, c) - current_sol_v > 0:
                                # print("Better value")
                                j = max_iter_j
                                i = -1
                                current_seq = modified_seq[:]
                            else:
                                j += 1
                        else:
                            j += 1
                else:
                    # if task is a predecessor of the neighbour: escape the j-loop
                    j = max_iter_j
            i += 1
        optimum = True
    return reassemble(current_seq, t, tsu, c)
