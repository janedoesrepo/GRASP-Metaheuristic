from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Counter, List

from task import Task


@dataclass(eq=False)
class Station(Sequence):
    task_list: List[Task] = field(default_factory=list)

    def __getitem__(self, i: int) -> Task:
        """Return the task at index of the Stations task list"""
        return self.task_list[i]
    
    def __len__(self) -> int:
        return len(self.task_list)
    
    def add(self, task: Task) -> None:
        """Adds a task to the Station"""
        self.task_list.append(task)
        
    def empty(self) -> bool:
        """Returns True if there are no tasks assigned to the Station"""
        return len(self) == 0
    
    def predecessor(self, other: Task) -> Task:
        """Return the predecessor of task in this station"""
        task_index = self.index(other)
        return self[task_index - 1]
    
    def fits_task(self, other: Task, cycle_time: int) -> bool:
        """Returns True if adding the task to the station does not exceed the cycle time
        TODO: Adding and removing the task is very inefficient. Find another solution.
        """
        
        self.add(other)
        station_time = self.get_time()
        self.task_list.remove(other)
        
        return station_time <= cycle_time
        
    def get_time(self) -> int:
        """Computes the time for a station to complete all tasks in its task list"""

        if self.empty():
            # An empty station has 0 station time
            return 0
        elif len(self) == 1:
            # A station with a single task only needs to process this task
            return self[0].processing_time
        else:
            # If a station has more than two tasks, setup times need to be considered
            per_task_values = [self.predecessor(task).setup_time(task) + task.processing_time for task in self]
            return sum(per_task_values)
