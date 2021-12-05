from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    id: int
    processing_time: int = field(compare=False)
    predecessors: List[int] = field(default_factory=list, init=False, repr=False, compare=False)
    setup_times: List[int]  = field(default_factory=list, init=False, repr=False, compare=False)
    
    def is_predecessor(self, other: Task) -> bool:
        """Returns True if self is a predecessor of other"""
        return self.id in other.predecessors
    
    def remove_predecessor(self, other: Task) -> None:
        """Remove a task from the list of predecessors
        
        TODO: instead of deleting predecessors, we could
        keep track of tasks that are are already in a solution.
        Then no copy of task lists would be necessary.
        """
        self.predecessors.remove(other.id)
    
    def setup_time(self, other: Task) -> int:
        """Returns the setup time from self to the task passed as an argument"""
        return self.setup_times[other.id]
