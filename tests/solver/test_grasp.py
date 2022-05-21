from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task import Task
from sualbsp_solver.data_model.task_list import TaskList
from sualbsp_solver.solver.grasp import GRASP


def test_get_greedy_indices_empty_station() -> None:
    tasks = TaskList([Task(0, 1), Task(1, 2)])
    station = Station(5)

    assert GRASP(1).get_greedy_indices(tasks, station) == [1.0, 0.5]


def test_get_greedy_indices_with_setups() -> None:
    station = Station(5)
    station.add_task(Task(0, 0, setup_times=[0, 1, 1]))

    tasks = TaskList([Task(1, 1), Task(2, 3)])
    assert GRASP(1).get_greedy_indices(tasks, station) == [0.5, 0.25]


def test_get_restricted_candidates() -> None:

    tasks = TaskList([Task(1, 1), Task(2, 3)])
    greedy_indices = [0.5, 0.25]

    assert (
        GRASP(1).get_restricted_candidates(tasks, greedy_indices, threshold=0.4)[0]
        == tasks[1]
    )
