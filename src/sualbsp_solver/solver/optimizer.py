from abc import ABC, abstractmethod

from sualbsp_solver.data_model import Graph, Station, TaskList


class OptimizationProcedure(ABC):
    """Abstract class that describes procedures by which a SUALBPS problem can be optimized.

    We differ between three types of optimization procedures:
        - the Station oriented strategy (SH),
        - the Task oriented strategy (TH), and
        - the GRASP Metaheuristics

    Ordering rules for candidate selection are:
        - Maximum setup time plus processing times (MaxTS)
        - Minimum setup time plus processing times (MinTS)
        - Maximum setup times (MaxS)
        - Minimum setup times (MinS)

    When we refer to strategy SH-MaxTS, we mean a station oriented strategy that selects next candidate tasks
    (those whose predecessors have already been assigned and can fit in the actual open station) by the
    MAXimum processing time plus setup time.

    Hence, the list of optimization pocedures that have been defined and tested are:
        - SH-MaxTS, SH-MaxS, SH-MinTS, SH-MinS and
        - TH-MaxTS, TH-MaxS, TH-MinTS, TH-MinS as well as
        - GRASP-5, GRASP-10
    """

    @abstractmethod
    def solve(self, instance: Graph) -> list[Station]:
        pass

    @abstractmethod
    def construct_solution(
        self, candidate_list: TaskList, cycle_time: int
    ) -> list[Station]:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__
