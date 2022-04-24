from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """Data model representing a task on the assembly line.

    Args:
        id: the task identifier
        processing_time: the time it takes the task to be completed
        predecessors: tasks that need to be completed before this task can be started
        setup_times: the setup times between this task and other tasks

    Returns:
        A task with its id and processing_time set

    Remarks:
        From a design perspective `add_predecessor` and `remove_predecessor`
        should not be calling `is_predecessor_of`.
    """

    id: int
    processing_time: int = field(compare=False)
    predecessors: list[int] = field(
        default_factory=list, init=False, repr=False, compare=False
    )
    setup_times: list[int] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    def add_predecessor(self, other: Task) -> None:
        """Adds other to the list of predecessors of self.

        If other already is a predecessor of self, do nothing.
        """
        if not other.is_predecessor_of(self):
            self.predecessors.append(other.id)

    def remove_predecessor(self, other: Task) -> None:
        """Remove other from the list of predecessors.

        If other is not a predecessor of self, do nothing.

        Remarks:
            instead of deleting predecessors, we could keep
            track of tasks that are are already in a solution.
            Then no copy of task lists would be necessary.
        """
        if other.is_predecessor_of(self):
            self.predecessors.remove(other.id)

    def is_predecessor_of(self, other: Task) -> bool:
        """Returns True if self is a predecessor of other."""
        return self.id in other.predecessors

    def setup_time_to(self, other: Task) -> int:
        """Returns the setup time from self to other.

        Remarks:
            using the setup_times list like a lookup table
            works because they are all set when the graph
            is parsed. Nonetheless, using a dictionary should
            be the better approach (quickfix, TODO).
        """
        return self.setup_times[other.id]
