from pathlib import Path
from time import perf_counter

from sualbsp_solver import in2_parser
from sualbsp_solver.solver.grasp import GRASP
from sualbsp_solver.solver.optimizer import OptimizationProcedure
from sualbsp_solver.solver.rule import get_ordering_rules
from sualbsp_solver.solver.station_oriented import StationOrientedStrategy
from sualbsp_solver.solver.task_oriented import TaskOrientedStrategy


def create_optimizers() -> list[OptimizationProcedure]:
    """Creates a list of all optimization procedures"""

    optimizers: list[OptimizationProcedure] = []
    ordering_rules = get_ordering_rules()
    for rule in ordering_rules:
        optimizers.append(StationOrientedStrategy(rule))
        optimizers.append(TaskOrientedStrategy(rule))

    for num_grasp_iterations in [5, 10]:
        optimizers.append(GRASP(num_grasp_iterations))

    return optimizers


class Experiment:
    """Model an experiment that takes a Graph instance and an optimizer to solve that instance"""

    def __init__(self, file_path: Path) -> None:
        self.graph = in2_parser.parse_graph(file_path)
        self.optimizers = create_optimizers()
        self.solutions: list[dict] = []

    def run(self) -> list[dict]:
        self.start_time = perf_counter()
        for optimizer in self.optimizers:

            optimizer_start_time = perf_counter()

            # Solve the instance using the optimizer
            stations = optimizer.solve(self.graph)

            self.solutions.append(
                {
                    "Instance": f"{self.graph}",
                    "Strategy": f"{optimizer}",
                    "Num_Stations": len(stations),
                    "Runtime": perf_counter() - optimizer_start_time
                    # TODO: Add the Sequence for export
                }
            )

        # Add best solution and compute Average Relative Deviation to each solution
        best_solution = self.best_solution()
        for solution in self.solutions:
            solution["Min_Stations"] = best_solution
            solution["ARD"] = self.compute_ARD(
                solution["Num_Stations"], solution["Min_Stations"]
            )

        return self.solutions

    def best_solution(self) -> int:
        """Returns the minimum number of stations from all solutions."""
        return min(solution["Num_Stations"] for solution in self.solutions)

    @staticmethod
    def compute_ARD(solution_stations: int, min_stations: int) -> float:
        """Compute the average relative deviation of a solution."""
        ARD = 100 * ((solution_stations - min_stations) / min_stations)
        return ARD
