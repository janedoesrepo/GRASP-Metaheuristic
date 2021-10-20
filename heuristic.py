import copy
from dataclasses import dataclass
from typing import List

from graph import GraphInstance
from rules import TaskOrderingRule
from station import Station
from strategies import OptimizationProcedure, StationOrientedStrategy, TaskOrientedStrategy


@dataclass
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
    strategy: OptimizationProcedure

    def __str__(self) -> str:
        if isinstance(self, (StationOrientedStrategy, TaskOrientedStrategy)):
            return f"{self.strategy}_{self.strategy.ordering_rule}"
        else:
            return f"{self.strategy}"

    def solve_instance(self, instance: GraphInstance) -> List[Station]:
        stations = self.strategy.solve(instance)
        return stations
