""" Heuristic rules for task assigment

 We differ between two Strategies:
  - Station oriented strategy heuristics (SH) and
  - Task oriented strategy heuristics (TH).

 Ordering rules for candidate selection are:
  - Maximum setup time plus processing times (max_ts)
  - Minimum setup time plus processing times (min_ts)
  - Maximum setup times (max_s)
  - Minimum setup times (min_s)

 When we refer to heuristic rule SH-max_ts we mean a Station oriented Heuristic that selects next task ordering
 candidate tasks (those whose predecessors have already been assigned and can fit in the actual open station) by
 MAXimum processing time plus Setup time.

 Hence, the list of heuristic rules that have been defined and tested are:
  - SH-max_ts, SH-max_s, SH-min_ts, SH-min_s and
  - TH-max_ts, TH-max_s, TH-min_ts, TH-min_s.
 """

# load system packages
from copy import deepcopy

# load own packages
from construction import buildCln, computeStationTime


def maxts(cln, station, t, tsu):
    lst = []
    for task in cln:
        if station:
            # s = time between last task assigned to the actual open station and the candidate task
            value = t[task] + tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # s = mean of all setup times between task an all other tasks
            value = t[task] + sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1], reverse=True)


def mints(cln, station, t, tsu):
    lst = []
    for task in cln:
        if station:
            # s = time between last task assigned to the actual open station and the candidate task
            value = t[task] + tsu[task][station[-1]]
            lst.append((task, value))
        elif not station:
            # s = mean of all setup times between task an all other tasks
            value = t[task] + sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1])


def maxs(cln, station, tsu):
    lst = []
    for task in cln:
        if station:
            # s = time between last task assigned to the actual open station and the candidate task
            value = tsu[station[-1]][task]
            # print('t(task %d) = tsu[station[-1]][task]:' % task, tsu[station[-1]][task])
            lst.append((task, value))
        elif not station:
            # s = mean of all setup times between task an all other tasks
            value = sum(tsu[task]) / (len(tsu[task])-1)
            # print('t(task %d) = sum(tsu[task]) / [len(tsu[task])-1]:' % task, sum(tsu[task]), '/', (len(tsu[task]) - 1))
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1], reverse=True)


def mins(cln, station, tsu):
    lst = []
    for task in cln:
        if station:
            # s = time between last task assigned to the actual open station and the candidate task
            value = tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # s = mean of all setup times between task an all other tasks
            value = sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1])


def orderTasks(procedure, cln, station, t, tsu):
    if 'max_ts' in procedure:
        return maxts(cln, station, t, tsu)
    elif 'min_ts' in procedure:
        return mints(cln, station, t, tsu)
    elif 'max_s' in procedure:
        return maxs(cln, station, tsu)
    elif 'min_s' in procedure:
        return mins(cln, station, tsu)
    else:
        print("No valid rule selected!")


def assignTask(station, task, cl, relations):
    station.append(task)  # Sequence random task in RCLn
    cl.remove(task)  # Remove this task from CL

    # Remove this task from Relations
    for relation in relations:
        if task in relation:
            relation.remove(task)


def heuristics(cl, relations, t, tsu, c, procedure):

    stations = [[]]     # initialise empty solution
    rel = deepcopy(relations)  # copy of relations needed for TH

    # as long as candidate list is not empty
    while cl:
        # use station oriented approach
        if 'SH' in procedure:
            # build CL_n for actual open station
            cln = buildCln(c, cl, relations, t, tsu, stations[-1])

            if not cln:  # if no task fits in actual open station
                stations.append([])  # open new empty station
                cln = buildCln(c, cl, relations, t, tsu, stations[-1])  # repeat building CL_n

            # order candidate tasks
            cln = orderTasks(procedure, cln, stations[-1], t, tsu)

            # assign first task in CL_n to actual open station
            assignTask(stations[-1], cln[0][0], cl, relations)

        # use task oriented approach
        elif 'TH' in procedure:

            # build CL_n for TH depending only on precedence relations
            cln = []
            for task in cl:
                # proceed only if all predecessors have been assigned
                if not relations[task]:
                    cln.append(task)

            # order candidate tasks
            cln = orderTasks(procedure, cln, stations[-1], t, tsu)

            # assign first task in CL_n to first station it fits in
            temp_rel = rel[cln[0][0]][:]
            for station in stations:
                # delete all task of actual station from precedence relations
                for task in station:
                    if task in temp_rel:
                        temp_rel.remove(task)

                # as soon as precedence relations of task are met, do station assignment
                if not temp_rel:
                    temp_station = station[:]
                    temp_station.append(cln[0][0])
                    if computeStationTime(temp_station, t, tsu) <= c:
                        # if task fits in station, assign task and break for-loop
                        assignTask(station, cln[0][0], cl, relations)
                        break
            else:
                # in case for-loop did not break the task did not fit in any open station
                stations.append([])     # open new station
                assignTask(stations[-1], cln[0][0], cl, relations)  # assign task to new station
        else:
            print("No valid strategy selected!")

    return stations
