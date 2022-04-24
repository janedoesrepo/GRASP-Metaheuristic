import pytest
from sualbsp_solver.data_model.task import Task


@pytest.fixture
def task1() -> Task:
    task = Task(1, 2)
    return task


@pytest.fixture
def task2() -> Task:
    task = Task(2, 3)
    return task


def test_task_is_predecessor(task1: Task, task2: Task) -> None:

    task2.predecessors = [task1.id]
    assert task1.is_predecessor_of(task2)

    task2.predecessors = [0, task1.id]
    assert task1.is_predecessor_of(task2)


def test_task_is_not_predecessor(task1: Task, task2: Task) -> None:

    assert not task1.is_predecessor_of(task2)


def test_add_and_remove_predecessor(task1: Task, task2: Task) -> None:

    task2.add_predecessor(task1)
    assert task1.is_predecessor_of(task2)
    task2.remove_predecessor(task1)
    assert not task1.is_predecessor_of(task2)


def test_remove_task_that_is_no_predecessor(task1: Task, task2: Task) -> None:

    task2.remove_predecessor(task1)
    assert not task1.is_predecessor_of(task2)


def test_setup_time_retrieval(task1: Task, task2: Task) -> None:

    setup_time_t1_t2 = 3
    task1.setup_times = [0, 0, setup_time_t1_t2]
    assert task1.setup_time_to(task2) == setup_time_t1_t2
