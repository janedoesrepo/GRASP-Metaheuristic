# use np.random.randint() for random numbers
import numpy as np


# compute greedy index g() for all task in list cln with respect to sequence pi_n
def g(cln, pi_n, t, tsu):
    greedy = []
    for task in cln:
        # if sequence is empty, tsu = 0
        if not pi_n:
            totaltime = t[task]
            # print("Sequence empty: task j =", task, "has total time t[j] =", totaltime,
            #      "| computeStationTime:", computeStationTime([task], t, NONE))
        else:
            pred = pi_n[-1] # last task in sequence
            totaltime = tsu[pred][task] + t[task]   # tsu[n][j] + t[j]
            # print("Last task", task, "has total time tsu[j][n]+t[j] =", tsu[pred][task]],
            #      "+", t[task], "=", totaltime, "| computeStationTime:",
            #      computeStationTime([task], t, NONE) + tsu[pred][task]])
        value = 1 / totaltime
        greedy.append((value, task))
        # print("Greedy Index für Aufgabe", task, "ist %.5f" % greedy[greedy.index((value, task))][0])
    return greedy


def task2station(rcln, station, cl, relations):
    # Return random integers from the “discrete uniform” distribution of the specified dtype in the “half-open”
    # interval [low, high). If high is None (the default), then results are from [0, low).
    task = rcln[np.random.randint(len(rcln))]
    # print("Aufgabe %d hinzugefügt" % task)

    station.append(task)    # Sequence random task in RCLn
    cl.remove(task)         # Remove this task from CL

    # Remove this task from Relations
    for relation in relations:
        if task in relation:
            relation.remove(task)


def computeStationTime(station, t, tsu):
    if not station:
        return 0
    else:
        t_station = 0
        for task in station:
            # print(task)
            # task is first in station
            if station.index(task) == 0:
                # print('Stationszeit = t:', t_station, '+', t[task])
                t_station += t[task]
            # task is last in station
            elif station.index(task) == len(station)-1:
                pred = station[station.index(task) - 1]
                succ = station[0]
                # print('Stationszeit += t + tsu(pred) + tsu(succ):', t_station, '+', t[task], '+', tsu[pred][task], '+', tsu[task][succ])
                t_station += t[task] + tsu[pred][task] + tsu[task][succ]
            else:
                pred = station[station.index(task) - 1]
                # print('Stationszeit += t:', t_station, '+', t[task], '+', tsu[pred][task])
                t_station += t[task] + tsu[pred][task]
        return t_station


def buildCln(c, cl, relations, t, tsu, station):

    # initialise empty candidate list n
    cln = []

    # Check if any task in cl fulfills precedence relations and fits in actual open station
    for task in cl:

        # if task has no predecessors (equals to predecessors have already been sequenced)
        if not relations[task]:
            temp_station = station[:]   # copy station temporarily
            temp_station.append(task)   # append task to temporary station

            # check if task fits in station
            if computeStationTime(temp_station, t, tsu) <= c:
                cln.append(task)    # add task to CLn
                # print('Aufgabe hinzugefügt:', task)
    return cln


def constructSolution(cl, relations, t, tsu, alpha, c):

    # Initialise solution with one empty station
    stations = [[]]

    n = 1 # keeps track of iterations
    while cl:  # while cl is not empty

        # Build candidate list of iteration n (CL_n)
        cln = buildCln(c, cl, relations, t, tsu, stations[-1])

        if not cln:  # if no task fits in actual open station
            stations.append([])  # open new empty station
            cln = buildCln(c, cl, relations, t, tsu, stations[-1])

        # compute Greedy-Index g() for tasks in CL_n
        greedy_index = g(cln, stations[-1], t, tsu)

        # Compute threshold function
        gmax, _ = max(greedy_index)
        gmin, _ = min(greedy_index)
        threshold = gmin + alpha * (gmax - gmin)

        # Build Restricted Candidate List
        rcln = [greedy_index[i][1] for i in range(len(cln)) if greedy_index[i][0] <= threshold]

        # add random task from rcln to actual open station
        task2station(rcln, stations[-1], cl, relations)

        # next iteration
        n += 1

    return stations
