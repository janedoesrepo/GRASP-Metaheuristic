from methods.rules_v2 import TaskOrderingRule
from .strategies_v2 import apply_strategy


class Heuristic_v2:
    """ Heuristic rules for task assigment

     We differ between two types of strategies:
      - Station oriented strategies (SH) and
      - Task oriented strategies (TH).

     Ordering rules for candidate selection are:
      - Maximum setup time plus processing times (max_ts)
      - Minimum setup time plus processing times (min_ts)
      - Maximum setup times (max_s)
      - Minimum setup times (min_s)

     When we refer to heuristic rule SH-max_ts we mean a station oriented heuristic that selects next task ordering
     candidate tasks (those whose predecessors have already been assigned and can fit in the actual open station) by
     MAXimum processing time plus setup time.

     Hence, the list of heuristic that have been defined and tested are:
      - SH-max_ts, SH-max_s, SH-min_ts, SH-min_s and
      - TH-max_ts, TH-max_s, TH-min_ts, TH-min_s.
     """

    def __init__(self, strategy, rule: TaskOrderingRule):
        self.name = f"{strategy}_{rule.__class__.__name__}"
        self.strategy = strategy
        self.rule = rule

    def apply(self, instance):
        stations = apply_strategy(self, instance)
        return stations
