import copy

from sualbsp_solver.data_model import Graph, Station, TaskList
from sualbsp_solver.solver.optimizer import OptimizationProcedure
from sualbsp_solver.solver.rule import TaskOrderingRule


class TaskOrientedStrategy(OptimizationProcedure):
    """The task-oriented procedure (TH) is an iterative procedure which, at each iteration and
    according to a priority rule, assigns one of a group of candidate tasks to a workstation.
    A task is considered a candidate once all of its preceding tasks have been assigned. The
    chosen task is assigned to the first workstation in which it can be assigned (provided
    that it fits in the workstation and that all of its preceding tasks have been assigned). All
    of the workstations remain open until all of the tasks have been assigned, at which point
    the procedure ends. [Martino & Pastor (2010), 3.3]

    TODO: Procedure seems to not be working correctly. How should the tasks be ordered if there are
    multiple stations they could be assigned to and the setup may change the ordering?"""

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

            # Condition 1: candidates are tasks that have no precedence relations
            candidates = task_list.without_predecessors()

            # order the list of station candidates
            ordered_candidates = self.ordering_rule.order_tasks(
                candidates, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates.first

            # assign next task to first station it fits in
            for station in stations:
                if not station.can_fit(next_task):
                    continue
                break
            else:
                # in case for-loop did not encounter a break-statement, else is invoked.
                # the chosen task did not fit in any open station -> open a new station
                stations.append(Station(cycle_time))  # open new station
                current_station = stations[-1]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            task_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            task_list.remove_from_predecessors(next_task)

        return stations
