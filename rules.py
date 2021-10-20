from abc import ABC, abstractmethod
from typing import List, Tuple
import statistics

from station import Station
from task import Task


class TaskOrderingRule(ABC):
    """Abstract class that decsribes a rule by which a list of tasks should be ordered."""

    @abstractmethod
    def order_tasks(self, candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
        pass

    def __str__(self):
        return self.__class__.__name__


class MaxTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time descending"""

    def order_tasks(self, candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
        tasks_with_values = setups_plus_processing(candidates, station)
        return sorted(tasks_with_values, key=lambda x: x[1], reverse=True)


class MinTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time ascending"""

    def order_tasks(self, candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
        tasks_with_values = setups_plus_processing(candidates, station)
        return sorted(tasks_with_values, key=lambda x: x[1])


class MaxSOrdering(TaskOrderingRule):
    """Orders tasks by setup time descending"""

    def order_tasks(self, candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
        tasks_with_values = setups_only(candidates, station)
        return sorted(tasks_with_values, key=lambda x: x[1], reverse=True)


class MinSOrdering(TaskOrderingRule):
    """Orders tasks by setup time ascending"""

    def order_tasks(self, candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
        tasks_with_values = setups_only(candidates, station)
        return sorted(tasks_with_values, key=lambda x: x[1])


def setups_plus_processing(candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
    """Return a tuple for each task in the candidate_list and its processing incl. setup time) """
    
    if not station.empty():
        return [(task, station.last().setup_time(task) + task.processing_time) for task in candidates]
    else:
        return [(task, task.processing_time + statistics.mean(task.setup_times)) for task in candidates]


def setups_only(candidates: List[Task], station: Station) -> List[Tuple[Task, float]]:
    """Return a tuple for each task in the candidate_list and its setup time """

    if not station.empty():
        # only the setup time between last task assigned to the current station and the candidate task
        return [(task, station.last().setup_time(task)) for task in candidates]
    else:
        # only the mean of all setup times between the candidate task an all other tasks
        return [(task, statistics.mean(task.setup_times)) for task in candidates]
