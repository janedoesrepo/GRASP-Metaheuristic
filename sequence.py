from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from station import Station
from task import Task
from typing import List


@dataclass
class TaskSequence(Sequence):
    task_list: List[Task]
    
    def __getitem__(self, key):
        """Returns the task at position key in the TaskSequence"""
        if isinstance(key, int):
            return self.task_list[key]
        elif isinstance(key, slice):
            return TaskSequence(self.task_list[key])
    
    def __len__(self) -> int:
        """Returns the numer of tasks in the TaskSequence"""
        return len(self.task_list)
    
    def reassemble(self, cycle_time: int) -> List[Station]:
        """Reassemble a list of tasks into a list of stations. A sequence is reassembled
        by assigning its tasks one by one to a station as long as the station does not
        exceed the cycle time. Once it does, open a new station and continue assigning."""

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
    
    @staticmethod
    def from_solution(solution) -> TaskSequence:
        return TaskSequence([task for station in solution for task in station])
    
    def swap_tasks(self, pos1: int, pos2: int) -> TaskSequence:
        """Returns a new sequence with the position of two tasks swapped"""
        new_sequence = self.task_list.copy()
        new_sequence[pos2] = self.task_list[pos1]
        new_sequence[pos1] = self.task_list[pos2]
        return TaskSequence(new_sequence)
