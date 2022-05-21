import pytest
from sualbsp_solver.data_model import Task
from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task_list import TaskList


def test_get_item_int() -> None:
    tasks = TaskList([Task(0, 0), Task(1, 0), Task(2, 0)])

    assert tasks[0] == Task(0, 0)


def test_get_item_slice() -> None:
    tasks = TaskList([Task(0, 0), Task(1, 0), Task(2, 0)])
    assert tasks[:2] == TaskList([Task(0, 0), Task(1, 0)])


def test_iteration_over_task_list() -> None:

    tasks = TaskList([Task(0, 0), Task(1, 0), Task(2, 0)])

    for task in tasks:
        assert task in tasks


def test_get_tasks_without_predecessors() -> None:

    tasks = TaskList([Task(0, 0, predecessors=[1]), Task(1, 0, predecessors=[])])
    assert tasks.get_tasks_without_predecessors()[0] == Task(1, 0)


def test_get_tasks_that_fit_station() -> None:

    station = Station(5)
    tasks = TaskList([Task(1, 3), Task(0, 6)])
    assert tasks.get_tasks_that_fit_station(station)[0] == Task(1, 3)


def test_remove_successful() -> None:

    to_be_removed = Task(0, 6)
    tasks = TaskList([Task(1, 3), to_be_removed])
    tasks.remove(to_be_removed)
    assert to_be_removed not in tasks
    assert Task(1, 3) in tasks


def test_remove_fails() -> None:
    with pytest.raises(ValueError):
        TaskList().remove(Task(0, 1))
