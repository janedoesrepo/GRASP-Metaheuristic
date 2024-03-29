from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import overload

from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task import Task


@dataclass
class TaskList(Sequence):
    _tasks: list[Task] = field(default_factory=list)

    @overload
    def __getitem__(self, index: int) -> Task:
        pass

    @overload
    def __getitem__(self, index: slice) -> TaskList:
        pass

    def __getitem__(self, index: int | slice) -> Task | TaskList:
        """Returns the task at index from the list. For slice a new TaskList is returned."""
        if isinstance(index, slice):
            return TaskList(self._tasks[index])
        else:
            return self._tasks[index]

    def __len__(self) -> int:
        """Returns the number of tasks in the list."""
        return len(self._tasks)

    def reassemble(self, cycle_time: int) -> list[Station]:
        """Reassemble the list of tasks into a list of stations according to the following strategy:
        Assign the tasks in the list one by one, starting at index 0,  to a station as long as the
        station does not exceed the cycle time. Once it does, open a new station and continue assigning."""

        solution: list[Station] = [Station(cycle_time)]
        current_station = solution[-1]

        for task in self._tasks:
            if current_station.can_fit(task):
                current_station.add_task(task)
            else:
                solution.append(Station(cycle_time))
                current_station = solution[-1]
                current_station.add_task(task)

        return solution

    def swap_tasks(self, pos1: int, pos2: int) -> TaskList:
        """Returns a new TaskList with the position of two tasks swapped"""
        new_sequence = self._tasks.copy()
        new_sequence[pos2] = self._tasks[pos1]
        new_sequence[pos1] = self._tasks[pos2]
        return TaskList(new_sequence)

    def get_tasks_without_predecessors(self) -> TaskList:
        """Returns a list of tasks that have no predecessors"""
        return TaskList([task for task in self._tasks if not len(task.predecessors)])

    def get_tasks_that_fit_station(self, station: Station) -> TaskList:
        """Returns a list of tasks that fit into the station"""
        return TaskList([task for task in self._tasks if station.can_fit(task)])

    def remove_from_predecessors(self, next_task: Task) -> None:
        """Removes the precedence relation of a newly sequenced tasked from all other tasks"""
        for task in self._tasks:
            if next_task.is_predecessor_of(task):
                task.remove_predecessor(next_task)

    def remove(self, task: Task) -> None:
        """Remove first occurrence of task.
        Raises ValueError if the task is not present."""
        try:
            self._tasks.remove(task)
        except ValueError as e:
            raise e

    @staticmethod
    def from_solution(solution: list[Station]) -> TaskList:
        """Returns a new TaskList created from a list of Stations."""
        return TaskList([task for station in solution for task in station])

    @property
    def first(self) -> Task:
        """Returns the Task at index 0 from the TaskList."""
        return self._tasks[0]
