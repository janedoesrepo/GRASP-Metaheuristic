from typing import List


def apply_rule(rule, instance, candidates, station) -> List:
    if rule == "max_ts":
        return setups_plus_processing(candidates, station, instance.setups, instance.processing_times, reverse=True)
    elif rule == "min_ts":
        return setups_plus_processing(candidates, station, instance.setups, instance.processing_times, reverse=False)
    elif rule == "max_s":   
        return setups_only(candidates, station, instance.setups, reverse=True)
    elif rule == "min_s":
        return setups_only(candidates, station, instance.setups, reverse=False)
    else:
        print("No valid rule selected!")


def setups_plus_processing(cln, station, tsu, t, reverse=None) -> List:
    lst = []
    for task in cln:
        if station:
            # time between last task assigned to the actual open station and the candidate task
            value = t[task] + tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # mean of all setup times between task an all other tasks
            value = t[task] + sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1], reverse=reverse)


def setups_only(cln, station, tsu, reverse=None) -> List:
    lst = []
    for task in cln:
        if station:
            # time between last task assigned to the actual open station and the candidate task
            value = tsu[station[-1]][task]
            lst.append((task, value))
        elif not station:
            # mean of all setup times between task an all other tasks
            value = sum(tsu[task]) / (len(tsu[task])-1)
            lst.append((task, value))
    return sorted(lst, key=lambda x: x[1], reverse=reverse)
