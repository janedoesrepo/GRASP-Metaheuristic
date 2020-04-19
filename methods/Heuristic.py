from. strategies import apply_strategy


def create_heuristics() -> list:
    strategies = ["SH", "TH"]
    rules = ["max_ts", "min_ts", "max_s", "min_s"]
    heuristics = [Heuristic(strategy, rule) for strategy in strategies for rule in rules]
    return heuristics


class Heuristic:
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
     MAXimum processing time plus Setup time.

     Hence, the list of heuristic that have been defined and tested are:
      - SH-max_ts, SH-max_s, SH-min_ts, SH-min_s and
      - TH-max_ts, TH-max_s, TH-min_ts, TH-min_s.
     """

    def __init__(self, strategy, rule):
        self.name = f"{strategy}_{rule}"
        self.strategy = strategy
        self.rule = rule

    def apply(self, instance):
        stations = apply_strategy(self, instance)
        return stations
