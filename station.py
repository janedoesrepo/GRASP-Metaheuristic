from collections.abc import Sequence
from dataclasses import dataclass, field
from task import Task
from typing import List


@dataclass(eq=False)
class Station(Sequence):
    
    cycle_time: int
    station_time: int = field(default=0, init=False)
    data: List[Task] = field(default_factory=list, init=False)
    
    def __getitem__(self, key):
        """Return the task at index of the Stations task list"""
        return self.data[key]
    
    def __len__(self):
        return len(self.data)
        
    def empty(self) -> bool:
        """Returns True if there are no tasks assigned to the Station"""
        return len(self) == 0
    
    def append(self, task: Task) -> None:
        """Append a Task object to the Station and update the station time"""
        if self.empty():
            self.station_time += task.processing_time       
        else:
            additional_time = self[-1].setup_time(task) + task.processing_time
            self.station_time += additional_time
        self.data.append(task)
    
    def fits_task(self, other: Task) -> bool:
        """Returns True if adding the task to the station does not exceed the cycle time"""
        if self.empty():
            return other.processing_time <= self.cycle_time       
        else:
            additional_time = self[-1].setup_time(other) + other.processing_time
            return self.station_time + additional_time <= self.cycle_time
