from dataclasses import dataclass, field
from typing import List

from task import Task


@dataclass(eq=False)
class Station:
    task_list: List[Task] = field(default_factory=list)
    
    def add(self, task: Task) -> None:
        """Adds a task to the Station"""
        self.task_list.append(task)
        
    def remove(self, task: Task) -> None:
        """Removes a task from the Station"""
        self.task_list.remove(task)
        
    def empty(self) -> bool:
        """Returns True if there are no tasks assigned to the Station"""
        return len(self.task_list) == 0
    
    def first(self) -> Task:
        """Returns the first task in the Station"""
        return self.task_list[0]
    
    def last(self) -> Task:
        """Returns the last task in the Station"""
        return self.task_list[-1]
    
    def predecessor(self, other: Task) -> Task:
        """Return the predecessor of task in this station"""
        task_index = self.task_list.index(other)
        return self.task_list[task_index - 1]
    
    def fits_task(self, other: Task, cycle_time: int) -> bool:
        """Returns True if adding the task to the station does not exceed the cycle time"""
        
        self.add(other)
        station_time = self.get_time()
        self.remove(other)
        
        return station_time <= cycle_time
        
    def get_time(self) -> int:
        """Computes the time for a station to complete all tasks in its task list"""

        if self.empty():
            # An empty station has 0 station time
            return 0
        elif len(self.task_list) == 1:
            # A station with a single task only needs to process this task
            return self.first().processing_time
        else:
            # If a station has more than two tasks, setup times need to be considered
            return sum([self.predecessor(task).setup_time(task) + task.processing_time for task in self.task_list])
        