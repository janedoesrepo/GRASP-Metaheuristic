from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task import Task


def test_add_task_successful() -> None:
    station = Station(5)
    station.add_task(Task(0, 3))
    assert station.task_list[0] == Task(0, 3)
    assert station.station_time == 3


def test_add_task_fails() -> None:
    station = Station(5)
    station.add_task(Task(0, 6))
    assert station.is_empty()
    assert station.station_time == 0
