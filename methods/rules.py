def max_ts(cln, station, t, tsu):
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


def min_ts(cln, station, t, tsu):
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


def max_s(cln, station, tsu):
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


def min_s(cln, station, tsu):
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
