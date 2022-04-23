import statistics
from abc import ABC, abstractmethod
from typing import List, Tuple

from sualbsp_solver.data_model import Station, Task, TaskList


class TaskOrderingRule(ABC):
    """Abstract class that decsribes a rule by which a list of tasks should be ordered."""

    @abstractmethod
    def order_tasks(self, candidates: TaskList, station: Station) -> TaskList:
        pass

    def __str__(self):
        return self.__class__.__name__


class MaxTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time descending"""

    def order_tasks(self, candidates: TaskList, station: Station) -> TaskList:
        tasks_values = setups_plus_processing(candidates, station)
        tasks_values_sorted = sorted(tasks_values, key=lambda x: x[1], reverse=True)
        return TaskList([task for task, _ in tasks_values_sorted])


class MinTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time ascending"""

    def order_tasks(self, candidates: TaskList, station: Station) -> TaskList:
        tasks_values = setups_plus_processing(candidates, station)
        tasks_values_sorted = sorted(tasks_values, key=lambda x: x[1])
        return TaskList([task for task, _ in tasks_values_sorted])


class MaxSOrdering(TaskOrderingRule):
    """Orders tasks by setup time descending"""

    def order_tasks(self, candidates: TaskList, station: Station) -> TaskList:
        tasks_values = setups_only(candidates, station)
        tasks_values_sorted = sorted(tasks_values, key=lambda x: x[1], reverse=True)
        return TaskList([task for task, _ in tasks_values_sorted]) 


class MinSOrdering(TaskOrderingRule):
    """Orders tasks by setup time ascending"""

    def order_tasks(self, candidates: TaskList, station: Station) -> TaskList:
        tasks_values = setups_only(candidates, station)
        tasks_values_sorted = sorted(tasks_values, key=lambda x: x[1])
        return TaskList([task for task, _ in tasks_values_sorted])


def setups_plus_processing(candidates: TaskList, station: Station) -> List[Tuple[Task, float]]:
    """Return a tuple for each task in the candidate_list and its processing incl. setup time) """
    
    if station.empty():
        return [(task, task.processing_time + statistics.mean(task.setup_times)) for task in candidates]
    else:
        return [(task, station[-1].setup_time(task) + task.processing_time) for task in candidates]


def setups_only(candidates: TaskList, station: Station) -> List[Tuple[Task, float]]:
    """Return a tuple for each task in the candidate_list and its setup time """
    
    if station.empty():
        return [(task, statistics.mean(task.setup_times)) for task in candidates]
    else:
        return [(task, station[-1].setup_time(task)) for task in candidates]
