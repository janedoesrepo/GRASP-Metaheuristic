from typing import List
import copy

from app_v2.graph import GraphInstance
from app_v2.rules import TaskOrderingRule
from app_v2.station import Station
from app_v2.strategies import OptimizationStrategy


class Heuristic:
    """Heuristic rules for task assigment

    We differ between two types of optimization strategies:
     - the Station oriented strategies (SH) and
     - the Task oriented strategies (TH).

    Ordering rules for candidate selection are:
     - Maximum setup time plus processing times (MaxTS)
     - Minimum setup time plus processing times (MinTS)
     - Maximum setup times (MaxS)
     - Minimum setup times (MinS)

    When we refer to heuristic rule SH-MaxTS, we mean a station oriented heuristic that selects next candidate tasks
    (those whose predecessors have already been assigned and can fit in the actual open station) by the
    MAXimum processing time plus setup time.

    Hence, the list of heuristic that have been defined and tested are:
     - SH-MaxTS, SH-MaxS, SH-MinTS, SH-MinS and
     - TH-MaxTS, TH-MaxS, TH-MinTS, TH-MinS.
    """

    def __init__(self, strategy: OptimizationStrategy, ordering_rule: TaskOrderingRule):
        self.strategy = strategy
        self.ordering_rule = ordering_rule

    def __str__(self):
        return f"{self.strategy}_{self.ordering_rule}"

    def solve_instance(self, instance: GraphInstance) -> List[Station]:

        print(f"Applying {self}")

        # get a mutable copy of the original task list
        candidate_list = copy.deepcopy(instance.tasks)

        # assign all tasks in candidate list to stations
        stations = self.strategy.assign_tasks(
            candidate_list, self.ordering_rule, instance.cycle_time
        )

        return stations
