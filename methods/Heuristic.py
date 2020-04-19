from copy import deepcopy
from .utils import *
from .rules import *


def create_heuristics() -> list:
    strategies = ["SH", "TH"]
    rules = ["max_ts", "min_ts", "max_s", "min_s"]
    heuristics = [Heuristic(strategy, rule) for strategy in strategies for rule in rules]
    return heuristics


def apply_rule(rule, instance, candidates, station):
    if rule == "max_ts":
        return max_ts(candidates, station, instance.processing_times, instance.setups)
    elif rule == "min_ts":
        return min_ts(candidates, station, instance.processing_times, instance.setups)
    elif rule == "max_s":
        return max_s(candidates, station, instance.setups)
    elif rule == "min_s":
        return min_s(candidates, station, instance.setups)
    else:
        print("No valid rule selected!")


class Heuristic:
    """ Heuristic rules for task assigment

     We differ between two types of strategies:
      - Station oriented strategies (SH) and
      - Task oriented strategies (TH).

     Ordering rules for candidate selection are:
      - Maximum setup time plus processing times (max_ts)
      - Minimum setup time plus processing times (min_ts)
      - Maximum setup times (max_s)
      - Minimum setup times (min_s)

     When we refer to heuristic rule SH-max_ts we mean a station oriented heuristic that selects next task ordering
     candidate tasks (those whose predecessors have already been assigned and can fit in the actual open station) by
     MAXimum processing time plus Setup time.

     Hence, the list of heuristic that have been defined and tested are:
      - SH-max_ts, SH-max_s, SH-min_ts, SH-min_s and
      - TH-max_ts, TH-max_s, TH-min_ts, TH-min_s.
     """

    def __init__(self, strategy, rule):
        self.name = f"{strategy}_{rule}"
        self.strategy = strategy
        self.rule = rule

    def apply(self, instance):
        stations = [[]]
        curr_station = stations[-1]

        # copies are needed for TH in order to not change the original lists
        candidate_list = instance.task_ids.copy()
        relations = deepcopy(instance.relations)

        # use station oriented approach
        if self.strategy == "SH":

            while candidate_list:

                # build candidate list for actual open station
                station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

                # if no task fits in actual open station then open new empty station and build a new candidate list
                if not station_candidates:
                    stations.append([])
                    curr_station = stations[-1]
                    station_candidates = get_candidates(instance, candidate_list, relations, curr_station)

                # order candidates
                station_candidates = apply_rule(self.rule, instance, station_candidates, curr_station)

                # assign first task in CL_n to actual open station
                assign_task(curr_station, station_candidates[0][0], candidate_list, relations)

        # use task oriented approach
        elif self.strategy == "TH":

            while candidate_list:

                # build CL_n for TH depending only on precedence relations
                station_candidates = []
                for task in candidate_list:
                    # proceed only if all predecessors have been assigned
                    if not relations[task]:
                        station_candidates.append(task)

                # order candidate tasks
                station_candidates = apply_rule(self.rule, instance, station_candidates, curr_station)

                # assign first task in CL_n to first station it fits in
                temp_rel = relations[station_candidates[0][0]][:]
                for station in stations:
                    # delete all tasks of actual station from precedence relations
                    for task in station:
                        if task in temp_rel:
                            temp_rel.remove(task)

                    # as soon as precedence relations of task are met, do station assignment
                    if not temp_rel:
                        temp_station = station[:]
                        temp_station.append(station_candidates[0][0])
                        if compute_station_time(temp_station, instance.processing_times,
                                                instance.setups) <= instance.cycle_time:
                            # if task fits in station, assign task and break for-loop
                            assign_task(station, station_candidates[0][0], candidate_list, relations)
                            break
                else:
                    # in case for-loop did not break the task did not fit in any open station
                    stations.append([])  # open new station
                    curr_station = stations[-1]
                    assign_task(curr_station, station_candidates[0][0], candidate_list, relations)
        else:
            print("No valid strategy selected!")

        return stations
