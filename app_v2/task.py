import copy
from dataclasses import dataclass, field
from typing import List


@dataclass()
class Task:
    id: int
    processing_time: int
    predecessors: List[int] = field(default_factory=list, init=False, repr=False)
    setup_times: List[int] = field(default_factory=list, init=False, repr=False)

    def has_predecessors(self) -> bool:
        """Returns True if the list of predecessors is not empty"""
        return len(self.predecessors)
    
    def has_predecessor(self, task) -> bool:
        """Return True if task is a predecessor of self"""
        return task.id in self.predecessors
    
    def remove_predecessor(self, task) -> None:
        """Remove a task from the list of predecessors"""
        self.predecessors.remove(task.id)
    
    def setup_time(self, task) -> int:
        """Returns the setup time from self to the task passed as an argument"""
        return self.setup_times[task.id]

    def __deepcopy__(self, memo):

        id_self = id(self)

        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                copy.deepcopy(self.id, memo), copy.deepcopy(self.processing_time, memo)
            )
            _copy.predecessors = self.predecessors.copy()
            _copy.setup_times = self.setup_times
        return _copy
