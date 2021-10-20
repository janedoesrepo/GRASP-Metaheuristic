from abc import ABC, abstractmethod
from typing import List

from rules import TaskOrderingRule
from station import Station
from task import Task


#TODO: the same functions happen in grasp...
def get_tasks_without_predecessors(candidates: List[Task]) -> List[Task]:
    """Returns a list of tasks that have no predecessors"""
    return [task for task in candidates if not task.has_predecessors()]


def get_fitting_tasks(candidates: List[Task], station: Station, cycle_time: int) -> List[Task]:
    """Returns a list of tasks that fit into the station"""
    return [task for task in candidates if station.fits_task(task, cycle_time)]


def remove_from_predecessors(next_task: Task, candidate_list: List[Task]) -> None:
    """Removes the precedence relation of a newly sequenced tasked from all other tasks"""
    [task.remove_predecessor(next_task) for task in candidate_list if next_task.is_predecessor(task)]


class OptimizationStrategy(ABC):
    """Abstract class that describes the strategy by which the solutions are optimized"""

    @abstractmethod
    def assign_tasks(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:
        pass

    def __init__(self, ordering_rule: TaskOrderingRule):
        self.ordering_rule = ordering_rule

    def __str__(self):
        return self.__class__.__name__


class StationOrientedStrategy(OptimizationStrategy):
    """The candidate tasks will be assigned to the current station if processing the task
    does not exceed the instances cycle time. Otherwise a new station is opened."""

    def assign_tasks(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station()]
        current_station = stations[-1]

        # For a solution all tasks need to be assigned to station
        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidate_tasks = get_tasks_without_predecessors(candidate_list)

            # Condition 2: tasks fit into the current station
            candidate_tasks = get_fitting_tasks(candidate_tasks, current_station, cycle_time)

            # if there are no candidates for the current station open a new empty station
            if not len(candidate_tasks):
                stations.append(Station())
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidate_value_list = self.ordering_rule.order_tasks(
                candidate_tasks, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            chosen_task = ordered_candidate_value_list[0][0]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add(chosen_task)
            candidate_list.remove(chosen_task)

            # Remove the chosen task as a predecessor from all other candidates
            remove_from_predecessors(chosen_task, candidate_list)

        return stations


class TaskOrientedStrategy(OptimizationStrategy):
    """The task-oriented procedure (TH) is an iterative procedure which, at each iteration and
    according to a priority rule, assigns one of a group of candidate tasks to a workstation.
    A task is considered a candidate once all of its preceding tasks have been assigned. The
    chosen task is assigned to the first workstation in which it can be assigned (provided
    that it fits in the workstation and that all of its preceding tasks have been assigned). All
    of the workstations remain open until all of the tasks have been assigned, at which point
    the procedure ends. [Martino & Pastor (2010), 3.3]

    TODO: Procedure is not working correctly. How should the tasks be ordered if there are
    multiple stations they could be assigned to and the setup may change the ordering?"""

    def assign_tasks(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station()]
        current_station = stations[-1]

        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidate_tasks = get_tasks_without_predecessors(candidate_list)

            # order the list of station candidates (TODO: what is the correct station argument?)
            ordered_candidate_value_list = self.ordering_rule.order_tasks(
                candidate_tasks, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            chosen_task = ordered_candidate_value_list[0][0]

            # assign chosen task to first station it fits in
            for station in stations:

                # if task does not fit in station, check the next station
                if not station.fits_task(chosen_task, cycle_time):
                    continue

                # else no need to check further stations
                break

            else:
                # in case for-loop did not encounter a break-statement, else is invoked.
                # the chosen task did not fit in any open station -> open a new station
                stations.append(Station())  # open new station
                current_station = stations[-1]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add(chosen_task)
            candidate_list.remove(chosen_task)

            # Remove the chosen task as a predecessor from all other candidates
            remove_from_predecessors(chosen_task, candidate_list)

        return stations
