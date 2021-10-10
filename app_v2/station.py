from dataclasses import dataclass, field
from typing import List

from app_v2.task import Task


@dataclass
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
    
    def predecessor(self, task: Task) -> Task:
        """Return the predecessor of task in this station"""
        task_index = self.task_list.index(task)
        return self.task_list[task_index - 1]
    
    def fits_task(self, task: Task, cycle_time: int) -> bool:
        """Returns True if adding the task to the station does not exceed the cycle time"""
        
        self.add(task)
        station_time = self.get_time()
        self.remove(task)
        
        return station_time <= cycle_time
        
    def get_time(self) -> int:
        """Computes the time that a station needs to complete all its tasks"""

        # An empty station has 0 station time
        if self.empty():
            return 0
        
        # A station with a single task only needs to process this task
        elif len(self.task_list) == 1:
            return self.first().processing_time

        # If a station has more than two tasks, setup times need to be considered
        else:
            station_time = 0
            for task in self.task_list:
                predecessor = self.predecessor(task)
                station_time += task.processing_time + predecessor.setup_time(task)

            return station_time
        