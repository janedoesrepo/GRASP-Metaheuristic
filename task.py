import copy
from dataclasses import dataclass, field
from typing import List
from __future__ import annotations


@dataclass
class Task:
    id: int
    processing_time: int
    predecessors: List[int] = field(default_factory=list, compare=False, init=False, repr=False)
    setup_times: List[int] = field(default_factory=list, compare=False, init=False, repr=False)

    def has_predecessors(self) -> bool:
        """Returns True if the list of predecessors is not empty"""
        return len(self.predecessors)
    
    def has_predecessor(self, other: Task) -> bool:
        """Returns True if other is a predecessor of self"""
        return other.id in self.predecessors
    
    def remove_predecessor(self, other: Task) -> None:
        """Remove a task from the list of predecessors"""
        self.predecessors.remove(other.id)
    
    def setup_time(self, other: Task) -> int:
        """Returns the setup time from self to the task passed as an argument"""
        return self.setup_times[other.id]

    def __deepcopy__(self, memo) -> Task:

        id_self = id(self)

        _copy = memo.get(id_self)
        if _copy is None:
            _copy = Task(
                copy.deepcopy(self.id, memo), copy.deepcopy(self.processing_time, memo)
            )
            _copy.predecessors = self.predecessors.copy()
            _copy.setup_times = self.setup_times
        return _copy
