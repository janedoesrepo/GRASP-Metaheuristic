from app_v2.graph import Task
from abc import ABC, abstractmethod
from typing import List, Tuple
import statistics


class TaskOrderingRule(ABC):
    """Abstract class that decsribes a rule by which a list of tasks should be ordered.

    Using an abstract class as decribed in the Strategy Pattern has several benefits:
    - There is no more need for if/else checking of which rule to apply
    - The addition of new rules is easy
    - Cleaner implementation of the has-a TaskOrderingRule relation in Heuristic

    On the downside this creates some boiler-plate code. Alternatively the TaskOrderingRules
    could be written in a functional adaption of the Strategy Pattern and passed as functions.
    """

    @abstractmethod
    def order_tasks(
        self, candidates: List[Task], station: List[Task]
    ) -> List[Tuple[Task, float]]:
        pass

    def __str__(self):
        return self.__class__.__name__


class MaxTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time descending"""

    def order_tasks(
        self, candidates: List[Task], station: List[Task]
    ) -> List[Tuple[Task, float]]:

        # calculate the processing times of each task if added to the station
        tasks_with_values = setups_plus_processing(candidates, station)

        return sorted(
            tasks_with_values, key=lambda task_value: task_value[1], reverse=True
        )


class MinTSOrdering(TaskOrderingRule):
    """Orders tasks by processing time plus setup time ascending"""

    def order_tasks(
        self, candidates: List[Task], station: List[Task]
    ) -> List[Tuple[Task, float]]:

        # calculate the processing times of each task if added to the station
        tasks_with_values = setups_plus_processing(candidates, station)

        return sorted(tasks_with_values, key=lambda task_value: task_value[1])


class MaxSOrdering(TaskOrderingRule):
    """Orders tasks by setup time descending"""

    def order_tasks(
        self, candidates: List[Task], station: List[Task]
    ) -> List[Tuple[Task, float]]:

        # calculate the setup times of each task if added to the station
        tasks_with_values = setups_only(candidates, station)

        return sorted(
            tasks_with_values, key=lambda task_value: task_value[1], reverse=True
        )


class MinSOrdering(TaskOrderingRule):
    """Orders tasks by setup time ascending"""

    def order_tasks(
        self, candidates: List[Task], station: List[Task]
    ) -> List[Tuple[Task, float]]:

        # calculate the setup times of each task if added to the station
        tasks_with_values = setups_only(candidates, station)

        return sorted(tasks_with_values, key=lambda task_value: task_value[1])


def setups_plus_processing(
    candidates: List[Task], station: List[Task]
) -> List[Tuple[Task, float]]:

    # calculate processing time plus...
    if len(station):
        # ... the setup time between last task assigned to the current station and the candidate task
        return [
            (task, task.processing_time + station[-1].setup_times[task.id])
            for task in candidates
        ]
    else:
        # ... the mean of all setup times between the candidate task an all other tasks
        return [
            (task, task.processing_time + statistics.mean(task.setup_times))
            for task in candidates
        ]


def setups_only(
    candidates: List[Task], station: List[Task]
) -> List[Tuple[Task, float]]:

    if len(station):
        # only the setup time between last task assigned to the current station and the candidate task
        return [(task, station[-1].setup_times[task.id]) for task in candidates]
    else:
        # only the mean of all setup times between the candidate task an all other tasks
        return [(task, statistics.mean(task.setup_times)) for task in candidates]
