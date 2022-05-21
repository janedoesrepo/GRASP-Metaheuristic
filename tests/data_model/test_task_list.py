from sualbsp_solver.data_model import Task


def test_get_item_int() -> None:
    task_list = [Task(0, 0), Task(1, 0), Task(2, 0)]

    assert task_list[0] == Task(0, 0)


def test_get_item_slice() -> None:
    task_list = [Task(0, 0), Task(1, 0), Task(2, 0)]

    assert task_list[:2] == [Task(0, 0), Task(1, 0)]


def test_iteration_over_task_list() -> None:

    task_list = [Task(0, 0), Task(1, 0), Task(2, 0)]

    for task in task_list:
        assert task in task_list
