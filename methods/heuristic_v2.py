from methods.rules_v2 import TaskOrderingRule
from .strategies_v2 import OptimizationStrategy


class Heuristic_v2:
    """ Heuristic rules for task assigment

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

    def __init__(self, strategy: OptimizationStrategy, rule: TaskOrderingRule):
        self.strategy = strategy
        self.ordering_rule = rule
        self.name = f"{strategy.__class__.__name__}_{rule.__class__.__name__}"

    def apply(self, instance):
        stations = self.strategy.solve_instance(instance, self.ordering_rule)
        return stations
