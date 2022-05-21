import copy

from sualbsp_solver.data_model import Graph, Station, TaskList
from sualbsp_solver.solver.optimizer import OptimizationProcedure
from sualbsp_solver.solver.rule import TaskOrderingRule


class StationOrientedStrategy(OptimizationProcedure):
    """The candidate tasks will be assigned to the current station if processing the task
    does not exceed the instances cycle time. Otherwise a new station is opened."""

    def __init__(self, ordering_rule: TaskOrderingRule) -> None:
        self.ordering_rule = ordering_rule

    def solve(self, instance: Graph) -> list[Station]:

        print(f"Applying {self} with {self.ordering_rule}")
        task_list = TaskList(copy.deepcopy(instance.tasks))
        solution = self.construct_solution(task_list, instance.cycle_time)
        return solution

    def construct_solution(self, task_list: TaskList, cycle_time: int) -> list[Station]:

        # initialize stations
        stations: list[Station] = [Station(cycle_time)]
        current_station = stations[-1]

        while len(task_list):

            # Condition 1: tasks have no precedence relations
            candidates = task_list.get_tasks_without_predecessors()

            # Condition 2: tasks fit into the current station
            candidates = candidates.get_tasks_that_fit_station(current_station)

            # if there are no candidates for the current station open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidates = self.ordering_rule.order_tasks(
                candidates, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates[0]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            task_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            task_list.remove_from_predecessors(next_task)

        return stations
