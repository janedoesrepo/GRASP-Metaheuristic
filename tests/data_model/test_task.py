from sualbsp_solver.data_model.task import Task


def test_is_predecessor_of() -> None:

    task1 = Task(0, 5, predecessors=[2])
    task2 = Task(2, 3)

    assert task2.is_predecessor_of(task1)


def test_remove_predecessor() -> None:
    "After removing the only predecessor, the list of predecessors should be empty."

    task1 = Task(0, 5, predecessors=[2])
    task2 = Task(2, 3)

    task1.remove_predecessor(task2)
    assert len(task1.predecessors) == 0


def test_get_setup_time_to_self() -> None:
    """The setup time to self should always be 0."""

    task1 = Task(0, 5, setup_times=[0, 4, 3])

    assert task1.setup_time(task1) == 0


def test_get_setup_time_to_other() -> None:
    """The setup time to self should always be 0."""

    task1 = Task(0, 5, setup_times=[0, 4, 3])
    task2 = Task(2, 4)

    assert task1.setup_time(task2) == 3


def test_task_compare() -> None:
    """Two Tasks should be considered equals, if their id matches."""
    task1 = Task(0, 3)
    task2 = Task(0, 5)
    assert task1 == task2
