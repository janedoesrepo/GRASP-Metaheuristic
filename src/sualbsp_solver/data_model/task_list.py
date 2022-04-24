from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import List

from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task import Task


@dataclass
class TaskList(Sequence):
    """Container for objects of type `Task`."""

    task_list: List[Task] = field(default_factory=list)

    def __getitem__(self, index: int | slice) -> Task | TaskList:
        """Returns the task at index from the list. For slice a new TaskList is returned."""
        if isinstance(index, int):
            return self.task_list[index]
        elif isinstance(index, slice):
            return TaskList(self.task_list[index])

    def __len__(self) -> int:
        """Returns the number of tasks in the TaskList."""
        return len(self.task_list)

    def reassemble(self, cycle_time: int) -> List[Station]:
        """Reassemble the list of tasks into a list of stations.

        The tasks in the TaskList are assigned to stations one by one.
        If a station is full (i.e. assigning the next task would exceed
        the cycle time), open a new station and continue reassembling.
        """

        solution: List[Station] = [Station(cycle_time)]
        current_station = solution[-1]

        for task in self.task_list:
            if current_station.can_fit(task):
                current_station.add_task(task)
            else:
                solution.append(Station(cycle_time))
                current_station = solution[-1]
                current_station.add_task(task)

        return solution

    def swap_tasks(self, pos1: int, pos2: int) -> TaskList:
        """Returns a new TaskList with the position of two tasks swapped.

        Remark:
            Check whether it is really necessary to copy the TaskList
            or not. Mutating the list might be sufficient.
        """
        new_sequence = self.task_list.copy()
        new_sequence[pos2] = self.task_list[pos1]
        new_sequence[pos1] = self.task_list[pos2]
        return TaskList(new_sequence)

    def without_predecessors(self) -> TaskList:
        """Returns only tasks that have no predecessors."""
        return TaskList([task for task in self.task_list if not len(task.predecessors)])

    def that_fit(self, station: Station) -> TaskList:
        """Returns only tasks that fit into the station."""
        return TaskList([task for task in self.task_list if station.can_fit(task)])

    def remove_from_predecessors(self, next_task: Task) -> None:
        """Removes the precedence relation of next_task from all other tasks."""
        for task in self.task_list:
            if next_task.is_predecessor_of(task):
                task.remove_predecessor(next_task)

    def greedy_indices(self, current_station: Station) -> List[float]:
        """Calculate the greedy index g() for all candidate tasks with respect to the current station."""
        if current_station.empty():
            return [1 / task.processing_time for task in self.task_list]
        else:
            return [
                1 / (current_station[-1].setup_time_to(task) + task.processing_time)
                for task in self.task_list
            ]

    def restricted_candidates(
        self, current_station: Station, alpha: float = 0.3
    ) -> TaskList:
        # compute the greedy-Index g() for each candidate task
        greedy_indices = self.greedy_indices(current_station)

        # Compute threshold function
        threshold = self.get_greedy_threshold(greedy_indices, alpha)

        # Find candidates that pass the threshold condition
        return TaskList(
            [
                task
                for task, greedy_index in zip(self.task_list, greedy_indices)
                if greedy_index <= threshold
            ]
        )

    def remove(self, task: Task) -> None:
        """Removes task from the TaskList."""
        self.task_list.remove(task)

    @staticmethod
    def get_greedy_threshold(greedy_indices: List[float], alpha: float) -> float:
        """Returns a threshold calcuated based on the greedy_indices and alpha."""
        gmin = min(greedy_indices)
        gmax = max(greedy_indices)
        return gmin + alpha * (gmax - gmin)

    @staticmethod
    def from_solution(solution: List[Station]) -> TaskList:
        """Returns a new TaskSequence created from a list of Stations."""
        return TaskList([task for station in solution for task in station])

    @property
    def first(self) -> Task:
        """Returns the Task at index 0 from the TaskList."""
        try:
            return self.task_list[0]
        except IndexError as e:
            raise e
