from dataclasses import dataclass, field
from typing import List

from app_v2.graph import Task


@dataclass
class Station:
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Adds a task to the Station"""
        self.tasks.append(task)
        
    def remove_task(self, task: Task) -> None:
        """Removes a task from the Station"""
        self.tasks.remove(task)
        
    def is_empty(self) -> bool:
        """Returns True if there are no tasks assigned to the Station"""
        return len(self.tasks) == 0
    
    def last(self) -> Task:
        """Returns the last tasks in the Station"""
        return self.tasks[-1]
    
    def fits_task(self, task: Task, cycle_time: int) -> bool:
        
        self.add_task(task)
        station_time = self.get_time()
        self.remove_task(task)
        
        if station_time <= cycle_time:
            return True
        else:
            return False
        
    def get_time(self) -> int:
        """Computes the time that a station needs to complete all its tasks"""

        if self.is_empty():
            return 0

        # TODO: modeling the last task as the predecessor of the first task should
        # allow a single function to compute all processing times and setups at once.
        station_time = 0
        for task_index, task in enumerate(self.tasks):

            if task_index == 0:
                # task is first in station: only use its own processing time
                station_time += task.processing_time

            elif task_index == len(self.tasks) - 1:
                # task is last in station
                predecessor = self.tasks[task_index - 1]
                successor = self.tasks[0]
                station_time += (
                    task.processing_time
                    + predecessor.setup_times[task.id]
                    + task.setup_times[successor.id]
                )

            else:
                # task is in between
                predecessor = self.tasks[task_index - 1]
                station_time += task.processing_time + predecessor.setup_times[task.id]

        return station_time
        