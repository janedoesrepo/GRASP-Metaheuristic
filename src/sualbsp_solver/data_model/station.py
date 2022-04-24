from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import List

from sualbsp_solver.data_model.task import Task


@dataclass(eq=False)
class Station(Sequence):
    cycle_time: int
    station_time: int = field(default=0, init=False)
    task_sequence: List[Task] = field(default_factory=list, init=False)

    def __getitem__(self, index):
        """Return the task at index of the Stations task list."""
        return self.task_sequence[index]

    def __len__(self) -> int:
        """Returns the numer of tasks in the Station."""
        return len(self.task_sequence)

    def _get_total_processing_time(self, task: Task) -> int:
        """Returns the total time needed to process the task in this station."""
        if self.empty():
            return task.processing_time
        else:
            return self[-1].setup_time_to(task) + task.processing_time

    def _update_station_time(self, task: Task) -> None:
        """Adds the time needed to process the task to the current station time."""
        additional_time = self._get_total_processing_time(task)
        self.station_time += additional_time

    def empty(self) -> bool:
        """Returns True if there are no tasks assigned to the Station."""
        return len(self) == 0

    def add_task(self, task: Task) -> None:
        """Append a Task object to the Station and update the station time."""
        self._update_station_time(task)
        self.task_sequence.append(task)

    def can_fit(self, task: Task) -> bool:
        """Returns True if adding the task to the station does not exceed the cycle time."""
        additional_time = self._get_total_processing_time(task)
        return self.station_time + additional_time <= self.cycle_time
