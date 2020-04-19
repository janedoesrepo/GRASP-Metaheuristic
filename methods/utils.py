def compute_station_time(station, processing_time, setups):
    if not station:
        return 0
    else:
        t_station = 0
        for task in station:

            # task is first in station
            if station.index(task) == 0:
                t_station += processing_time[task]

            # task is last in station
            elif station.index(task) == len(station)-1:
                pred = station[station.index(task) - 1]
                succ = station[0]
                t_station += processing_time[task] + setups[pred][task] + setups[task][succ]

            # task is in between
            else:
                pred = station[station.index(task) - 1]
                t_station += processing_time[task] + setups[pred][task]
        return t_station


def get_candidates(instance, station_candidates, relations, station):
    """ Check if any task in the candidate_list fulfills all precedence relations and fits in actual open station """

    candidates = []
    for task in station_candidates:

        # if task has no (more) predecessors it can be sequenced
        if not relations[task]:
            temp_station = station.copy()
            temp_station.append(task)

            # check if task fits in station
            if compute_station_time(temp_station, instance.processing_times, instance.setups) <= instance.cycle_time:
                candidates.append(task)

    return candidates


def assign_task(station, task, candidate_list, relations):
    station.append(task)  # Sequence random task in RCLn
    candidate_list.remove(task)  # Remove this task from CL

    # Remove this task from relations
    # TODO when using list comprehension here then deepcopy might not be necessary
    for relation in relations:
        if task in relation:
            relation.remove(task)